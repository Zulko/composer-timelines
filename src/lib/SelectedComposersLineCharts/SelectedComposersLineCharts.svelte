<script>
  import ComposerLineChart from "./ComposerLineChart.svelte";

  export let selectedComposerData;
  let xMin;
  let xMax;

  $: {
    xMin = Math.min(
      ...selectedComposerData.map((composerData) => composerData.birth_year)
    );
    xMax = Math.max(
      ...selectedComposerData.map((composerData) => composerData.death_year)
    );
  }
</script>

<div style="margin-top: 1em">
  {#each selectedComposerData as composerData}
    <ComposerLineChart {composerData} {xMin} {xMax} />
  {/each}
</div>
