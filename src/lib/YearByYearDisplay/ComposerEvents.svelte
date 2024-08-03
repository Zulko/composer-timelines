<script>
  export let composerData;
  export let showWorks = true;
  export let showLifeEvents = true;
  export let makeItFunny = false;
  export let year;

  let sectionId;
  let nthYear;

  $: {
    sectionId = `${encodeURIComponent(composerData.full_name)}-${year}`;
    nthYear = withOrdinalSuffix(year - composerData.birth_year + 1);
  }
  function youtubeSearchUrl(composition) {
    const term = composerData.full_name + " " + composition.title;
    const encodedTerm = encodeURIComponent(term);
    return `https://www.youtube.com/results?search_query=${encodedTerm}`;
  }

  function withOrdinalSuffix(number) {
    // Convert number to an integer
    const n = Math.abs(number);
    const lastDigit = n % 10;
    const lastTwoDigits = n % 100;

    if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
      return number + "th";
    }

    switch (lastDigit) {
      case 1:
        return number + "st";
      case 2:
        return number + "nd";
      case 3:
        return number + "rd";
      default:
        return number + "th";
    }
  }
</script>

<div class="composer-events" id={sectionId}>
  {#if composerData.events.length > 0 || composerData.works.length > 0}
    <h4>
      {composerData.full_name} <span class="nth-year">— {nthYear} year </span>
    </h4>
  {/if}
  {#if showLifeEvents}
    <ul>
      {#each composerData.events as event}
        <li class="event-icon">
          {#if event.emoji}
            {event.emoji}
          {/if}
          <b
            >{event.title}
            {#if event.location}
              ({event.location})
            {/if}</b
          >
          {makeItFunny ? event.fun_version || "" : event.summary || ""} (<a
            href="{composerData.wikipedia_url}#{event.section}"
            target="_blank"
          >
            <i class="fab fa-wikipedia-w"></i>
            learn more</a
          >)
        </li>
      {/each}
    </ul>
  {/if}
  {#if showWorks}
    <ul class="works">
      {#each composerData.works as composition}
        <li>
          <a
            href={composition.imslp_url}
            class="icon"
            target="_blank"
            title="IMSLP link"
          >
            <i class="fas fa-file-pdf"></i>
          </a>
          <a
            href={youtubeSearchUrl(composition)}
            class="icon"
            target="_blank"
            title="Search YouTube"
          >
            <i class="fab fa-youtube"></i>
          </a>
          {composition.title}
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .composer-events ul {
    list-style-type: none;
    padding: 0;
  }

  .composer-events li {
    margin-bottom: 10px;
    /* padding-left: 25px; Adjust padding to accommodate the icon */

    position: relative;
  }

  .nth-year {
    font-weight: normal;
  }

  /* Icon for compositions */
</style>
