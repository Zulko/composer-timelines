<script>
  import { createEventDispatcher } from "svelte";
  import Select from "svelte-select";

  export let composerListWithMetadata = [];
  export let selectedComposers;

  const dispatch = createEventDispatcher();

  function handleChange(selectedOptions) {
    const selectedComposers = selectedOptions.map((option) => option.value);
    dispatch("selectionChange", selectedComposers);
  }

  function handleUnselect(unselected) {
    dispatch("unselected", unselected.value);
  }
</script>

<Select
  items={composerListWithMetadata
    .sort((composer) => composer.last_name)
    .map((composer) => ({
      label: `${composer.last_name}, ${composer.first_names}`,
      value: composer.full_name,
    }))}
  multiple={true}
  value={selectedComposers}
  on:change={(e) => handleChange(e.detail)}
  on:clear={(e) => handleUnselect(e.detail)}
  placeholder="Select composers"
/>
