<script>
  export let events;
</script>

<div class="world-events">
  {#if events.length > 0}
    <h4>In the world...</h4>
  {/if}
  <ul>
    {#each events as event}
      <li class="event">
        <b>{event.title} ({event.city}, {event.country})</b>
        {event.summary}
      </li>
    {/each}
    <li>
      <a
        href="https://en.wikipedia.org/wiki/{events[0].year}"
        class="icon"
        target="_blank"
        title="Go to Wikipedia"
      >
        <i class="fab fa-wikipedia-w"></i>
        Learn more...
      </a>
    </li>
  </ul>
</div>

<style>
  /* .world-events {
    color: rgb(22, 22, 22);
  } */
</style>
