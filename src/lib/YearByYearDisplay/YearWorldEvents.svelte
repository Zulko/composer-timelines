<script>
  export let events;
</script>

<div class="world-events">
  {#if events.length > 0}
    <h3>
      <a
        href="https://en.wikipedia.org/wiki/{events[0].year}"
        class="icon"
        target="_blank"
        title="Go to Wikipedia"
      >
        <i class="fab fa-wikipedia-w"></i>
      </a>
      In the world...
    </h3>
  {/if}
  <ul>
    {#each events as event}
      <li class="event-icon">
        <b>{event.event} ({event.city}, {event.country})</b>
        {event.summary}
      </li>
    {/each}
  </ul>
</div>

<style>
  .world-events {
    color: gray;
  }

  .event {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
  }

  .event h4 {
    margin: 0 0 5px;
    color: #333;
  }

  .event p {
    margin: 0;
    color: #555;
  }
</style>
