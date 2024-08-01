<script>
  import { onMount } from "svelte";
  import ComposerSelector from "./lib/ComposerSelector.svelte";
  import YearByYearDisplay from "./lib/YearByYearDisplay/YearByYearDisplay.svelte";
  import About from "./lib/About.svelte";
  import SelectedComposersLineCharts from "./lib/SelectedComposersLineCharts/SelectedComposersLineCharts.svelte";

  let composerListWithMetadata = [];
  let selectedComposers = [];
  let composerData = {};
  let worldEvents = {};
  let selectedComposerData = [];
  let urlProcessed = false;

  const baseFolder =
    process.env.NODE_ENV === "development" ? "" : "/composer-timelines";

  const dataFolder = baseFolder + "/data/";

  async function onSelectChange(selectedComposers) {
    console.log(`Count changed to: ${selectedComposers}`);
    for (const composer of selectedComposers) {
      if (!composerData[composer]) {
        const response = await fetch(
          dataFolder + `composer_data/${composer}.json`
        );
        const data = await response.json();
        composerData = { ...composerData, [composer]: data };
      }
    }
    if (urlProcessed) {
      updateURL();
    }
    // Your logic here
  }

  // Reactive statement that depends only on `count`
  $: selectChanged = selectedComposers; // Assigning count to a new reactive variable
  $: if (selectChanged) onSelectChange(selectChanged);

  $: {
    let selectedComposersWithData = selectedComposers.filter(
      (c) => composerData[c]
    );
    selectedComposersWithData.sort(
      (a, b) => composerData[a].birth_year - composerData[b].birth_year
    );

    selectedComposerData = selectedComposersWithData.map(
      (composer) => composerData[composer]
    );
  }

  onMount(async () => {
    syncWithUrl();

    const composerListResponse = await fetch(dataFolder + "composers.json");
    composerListWithMetadata = await composerListResponse.json();
    composerListWithMetadata.sort((a, b) => a.birth_year - b.birth_year);

    const worldEventsResponse = await fetch(dataFolder + "world_events.json");
    worldEvents = await worldEventsResponse.json();

    window.addEventListener("popstate", syncWithUrl);

    // Initial synchronization with the URL

    // return () => {
    //   window.removeEventListener("popstate", syncWithUrl);
    // };
  });

  function syncWithUrl() {
    const params = new URLSearchParams(window.location.search);
    const itemsFromUrl = params.get("selectedComposers");
    console.log({ itemsFromUrl });
    if (itemsFromUrl) {
      selectedComposers = itemsFromUrl.split(",");
    }
    urlProcessed = true;
  }

  async function handleSelection(event) {
    selectedComposers = event.detail;
  }

  function handleUnselect(event) {
    console.log({ event });
    selectedComposers = selectedComposers.filter(
      (e) => event.detail & (e != event.detail)
    );
  }

  function updateURL() {
    const url = new URL(window.location);
    if (selectedComposers.length === 0) {
      url.searchParams.delete("selectedComposers");
    } else {
      url.searchParams.set("selectedComposers", selectedComposers.join(","));
    }
    window.history.pushState({}, "", url);
  }
</script>

<main>
  <h1>Composer Timelines</h1>
  <About />
  <ComposerSelector
    {composerListWithMetadata}
    {selectedComposers}
    on:selectionChange={handleSelection}
    on:unselected={handleUnselect}
  />

  {#if selectedComposers.length > 0}
    <SelectedComposersLineCharts {selectedComposerData} />
    <YearByYearDisplay {selectedComposerData} {worldEvents} />
  {/if}
</main>

<style>
  /* Add your styles here for a modern look */
  h1 {
    text-align: center;
    margin-bottom: 1em;
  }
  main {
    font-family: "Lato", sans-serif !important;
    margin: 0;
    padding: 0;
  }
  :root,
  ::backdrop {
    --border: initial !important;
  }
</style>
