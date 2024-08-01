<script>
  import { chart } from "svelte-apexcharts";
  import { sineIn } from "svelte/easing";
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

    // Find the minimum and maximum year
    let minYear = Math.min(...allYearsSet);
    let maxYear = Math.max(...allYearsSet);

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
        custom: function () {
          return `<div></div>`;
        },
        x: { show: false, format: "click !" }, // This disables all tooltips
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
  console.log({ composerData, xMin, xMax });

  // Function to count items by year
  function countByYear(data) {
    return data.reduce((acc, { year }) => {
      acc[year] = (acc[year] || 0) + 1;
      return acc;
    }, {});
  }
</script>

<div use:chart={chartOptions} />
