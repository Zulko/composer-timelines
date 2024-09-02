<script>
  import { chart } from "svelte-apexcharts";
  export let composerData;
  export let xMin;
  export let xMax;
  console.log(composerData);
  let chartOptions = {};

  $: {
    // Count events and works by year
    let eventsByYear = countByYear(composerData.events);
    let worksByYear = countByYear(composerData.works);

    // Extract unique years and sort them
    let allYearsSet = new Set([
      ...Object.keys(eventsByYear),
      ...Object.keys(worksByYear),
    ]);

    // Convert years to numbers and find the minimum and maximum
    let allYearsArray = Array.from(allYearsSet).map(Number);
    let minYear = Math.min(...allYearsArray);
    let maxYear = Math.max(...allYearsArray);

    // Generate a full range of years from min to max
    let allYears = [];
    let combinedByYear = {};
    for (let year = minYear; year <= maxYear; year++) {
      allYears.push(year.toString());
      let eventsTotal = worksByYear[year] || 0;
      combinedByYear[year] = Math.sqrt(eventsTotal);
    }

    allYears.sort();

    let chartData = allYears.map((year) => ({
      x: year,
      y: combinedByYear[year],
    }));

    chartOptions = {
      dataLabels: {
        enabled: false,
      },
      chart: {
        type: "area",
        height: 100,
        zoom: {
          enabled: false,
        },
        toolbar: {
          show: false, // This hides the toolbar, including the download menu
        },
        events: {
          markerClick: (event, chartContext, opts) => {
            // Get the x value of the selected data point
            console.log({ opts });
            const xValue =
              opts.w.config.series[opts.seriesIndex].data[opts.dataPointIndex]
                .x;

            // Navigate to the section with the corresponding ID
            console.log("ddddddd");
            const composerURI = encodeURIComponent(composerData.full_name);
            window.location.hash = `#${composerURI}-${xValue}`;
          },
        },
      },
      tooltip: {
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
          const timestamp = w.globals.seriesX[seriesIndex][dataPointIndex];
          const date = new Date(timestamp);
          const year = date.getFullYear() + 1;
          const events = composerData.events.filter((e) => e.year === year);
          const works = composerData.works.filter((w) => w.year === year);

          let content = `<div class="custom-tooltip">
            <strong>${year}</strong><br>`;

          if (events.length > 0) {
            content += `<strong>Events:</strong><br>
            ${events.map((e) => `- ${e.title}`).join("<br>")}`;
          }

          if (works.length > 0) {
            content += `${events.length > 0 ? "<br><br>" : ""}
            <strong>Works:</strong><br>`;

            const displayedWorks = works.slice(0, 3);
            content += displayedWorks.map((w) => `- ${w.title}`).join("<br>");

            if (works.length > 3) {
              content += `<br>and ${works.length - 3} other${works.length - 3 > 1 ? "s" : ""}`;
            }
          }

          content += "</div>";
          return content;
        },
      },
      series: [
        {
          name: "Events",
          data: chartData,
        },
      ],
      xaxis: {
        type: "datetime",
        min: new Date(xMin, 0, 1).getTime(),
        max: new Date(xMax, 0, 1).getTime(),
        tooltip: {
          enabled: false,
        },
      },
      yaxis: {
        show: false,
        max: Math.max(...chartData.map((d) => d.y)),
      },
      title: {
        text: composerData.full_name,
        offsetY: 20,
      },
      grid: {
        show: false, // This hides all grid lines
      },
    };
  }

  // Function to count items by year
  function countByYear(data) {
    return data.reduce((acc, { year }) => {
      acc[year] = (acc[year] || 0) + 1;
      return acc;
    }, {});
  }
</script>

<div use:chart={chartOptions} />

<style>
  :global(.custom-tooltip) {
    padding: 10px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 12px;
  }
</style>
