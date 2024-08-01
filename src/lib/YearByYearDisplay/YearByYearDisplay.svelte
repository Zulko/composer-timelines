<script>
  import ComposerEvents from "./ComposerEvents.svelte";
  import YearWorldEvents from "./YearWorldEvents.svelte";

  export let selectedComposerData;
  export let worldEvents;

  let dataByYearToDisplay;
  let showLifeEvents = true;
  let showWorks = true;
  let showWorldEvents = false;
  let makeItFunny = false;

  $: {
    let yearsSet = new Set();
    selectedComposerData.forEach((composerData) => {
      composerData.events.forEach((event) => yearsSet.add(event.year));
      composerData.works.forEach((composition) =>
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
      selectedComposers: selectedComposerData.map((composerData) => ({
        ...composerData,
        events: composerData.events.filter((e) => e.year === year),
        works: composerData.works.filter((c) => c.year === year),
      })),
    }));
  }
</script>

<div class="year-by-year-display">
  <center>
    <h2>Chronology</h2>
    <div class="checkbox-container">
      <label for="life-events"
        ><input
          type="checkbox"
          id="life-events"
          bind:checked={showLifeEvents}
        /> Life events</label
      >

      <label for="works"
        ><input type="checkbox" id="works" bind:checked={showWorks} /> Works</label
      >

      <label for="world-events"
        ><input
          type="checkbox"
          id="world-events"
          bind:checked={showWorldEvents}
        />
        World events</label
      >

      <label for="make-it-funny"
        ><input type="checkbox" id="make-it-funny" bind:checked={makeItFunny} />
        Make it funny!</label
      >
    </div>
  </center>
  {#each dataByYearToDisplay as yearData}
    <h3>{yearData.year}</h3>
    <!-- <hr /> -->
    {#each yearData.selectedComposers as composerData}
      <ComposerEvents
        {composerData}
        {showWorks}
        {showLifeEvents}
        {makeItFunny}
        year={yearData.year}
      />
    {/each}
    {#if showWorldEvents}
      <YearWorldEvents events={yearData.worldEvents} />
    {/if}
  {/each}
</div>

<style>
  textarea,
  select,
  input {
    margin-left: 1em;
    background-color: var(--bg);
    border: 1px solid grey;
  }

  .checkbox-container {
    margin-top: 1em;
  }

  h3 {
    padding-bottom: 10px;
    border-bottom: 0.5px solid #000; /* Line thickness and color */
  }

  label {
    display: inline-block;
  }
</style>
