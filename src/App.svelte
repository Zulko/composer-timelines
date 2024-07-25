<script>
  import { onMount } from "svelte";
  import ComposerSelector from "./lib/ComposerSelector.svelte";
  import YearByYearDisplay from "./lib/YearByYearDisplay.svelte";
  import About from "./lib/About.svelte";

  let composerListWithMetadata = [];
  let selectedComposers = [];
  let composerData = {};
  let worldEvents = {};

  const baseFolder =
    process.env.NODE_ENV === "development" ? "" : "/composer-timelines";

  let dataByYearToDisplay = [];

  $: {
    // compute the years to display information for
    let yearsSet = new Set();
    selectedComposers
      .filter((c) => composerData[c])
      .forEach((composer) => {
        composerData[composer].events.forEach((event) =>
          yearsSet.add(event.year)
        );
        composerData[composer].compositions.forEach((composition) =>
          yearsSet.add(composition.year)
        );
      });
    let yearsToDisplay = Array.from(yearsSet)
      .filter((year) => year)
      .sort((a, b) => a - b);

    // compute the data to be displayed
    dataByYearToDisplay = yearsToDisplay.map((year) => ({
      year,
      worldEvents: worldEvents[year],
      selectedComposers: selectedComposers
        .filter((c) => composerData[c])
        .map((composer) => ({
          full_name: composer,
          last_name: composerData[composer].last_name,
          wikipedia_url: composerData[composer].wikipedia_url,
          events: composerData[composer].events.filter(
            (event) => event.year === year
          ),
          compositions: composerData[composer].compositions.filter(
            (composition) => composition.year === year
          ),
        })),
    }));
  }

  onMount(async () => {
    const composerListResponse = await fetch(
      baseFolder + "/data/composer_list_with_metadata.json"
    );
    composerListWithMetadata = await composerListResponse.json();

    const worldEventsResponse = await fetch(
      baseFolder + "/data/year_world_events.json"
    );
    worldEvents = await worldEventsResponse.json();
  });

  async function handleSelection(event) {
    selectedComposers = event.detail;
    for (const composer of selectedComposers) {
      if (!composerData[composer]) {
        const response = await fetch(
          `${baseFolder}/data/composer_data/${composer}.json`
        );
        const data = await response.json();
        composerData = { ...composerData, [composer]: data };
      }
    }
  }

  function handleUnselect(event) {
    selectedComposers = selectedComposers.filter((e) => e != event.detail);
  }
</script>

<main>
  <h1>Composer Timelines</h1>
  <ComposerSelector
    {composerListWithMetadata}
    on:selectionChange={handleSelection}
    on:unselected={handleUnselect}
  />
  <YearByYearDisplay {dataByYearToDisplay} />
  <About />
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
