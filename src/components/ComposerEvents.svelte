<script>
  export let composerData;
  export let showWorks = true;
  export let showLifeEvents = true;

  function youtubeSearchTerm(composition) {
    return encodeURIComponent(composerData.last_name + " " + composition.title);
  }
</script>

<div class="composer-events">
  {#if composerData.events.length > 0 || composerData.compositions.length > 0}
    <h3>
      <a
        href={composerData.wikipedia_url}
        class="icon"
        target="_blank"
        title="Go to Wikipedia"
      >
        <i class="fab fa-wikipedia-w"></i>
      </a>
      {composerData.full_name}
    </h3>
  {/if}
  {#if showLifeEvents}
    <ul>
      {#each composerData.events as event}
        <li class="event-icon">
          <b>{event.event} ({event.city}, {event.country})</b>
          {event.summary}
        </li>
      {/each}
    </ul>
  {/if}
  {#if showWorks}
    <ul class="works">
      {#each composerData.compositions as composition}
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
            href="https://www.youtube.com/results?search_query={youtubeSearchTerm(
              composition
            )}"
            class="icon"
            target="_blank"
            title="Search YouTube"
          >
            <i class="fab fa-youtube"></i>
          </a>
          <!-- <a
            href="https://open.spotify.com/search/{youtubeSearchTerm(
              composition
            )}"
            class="icon"
            target="_blank"
            title="Search Spotify"
          >
            <i class="fab fa-spotify"></i>
          </a> -->
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
    padding-left: 25px; /* Adjust padding to accommodate the icon */
    position: relative;
  }

  /* Icon for events */
  .composer-events .event-icon::before {
    content: "\f1ea"; /* Unicode for Font Awesome 'book' icon */
    font-family: "Font Awesome 5 Free";
    font-weight: 900; /* Font Awesome free icons have a font-weight of 900 */
    position: absolute;
    left: 0;
    top: 0;
    font-size: 1rem;
    color: #555;
  }

  /* Icon for compositions */
</style>
