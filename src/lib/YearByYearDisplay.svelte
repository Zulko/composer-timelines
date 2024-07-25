<script>
  import ComposerEvents from "./ComposerEvents.svelte";
  import YearWorldEvents from "./YearWorldEvents.svelte";
  export let dataByYearToDisplay;

  let showLifeEvents = true;
  let showWorks = true;
  let showWorldEvents = true;
</script>

<div class="year-by-year-display">
  <div class="checkbox-container">
    <input type="checkbox" id="life-events" bind:checked={showLifeEvents} />
    <label for="life-events">Life events</label>

    <input type="checkbox" id="works" bind:checked={showWorks} />
    <label for="works">Works</label>

    <input type="checkbox" id="world-events" bind:checked={showWorldEvents} />
    <label for="world-events">World events</label>
  </div>
  {#each dataByYearToDisplay as yearData}
    <h2>{yearData.year}</h2>
    {#each yearData.selectedComposers as composerData}
      <ComposerEvents {composerData} {showWorks} {showLifeEvents} />
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
</style>
