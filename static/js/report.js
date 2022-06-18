var endpoint = 'api/reportData/';
  
$.ajax({
  method: "GET",
  url: endpoint,
  success: function(graphData) {
    console.log("Graph data loaded");
    salesPerformanceGraph(graphData.sales_performance, "graph1");
    profitLossGraph(graphData.profit_and_loss, "graph3");
    inflowOutflowGraph(graphData.cash_inflow_outflow, "graph4");
    runwayGraph(graphData.runaway, "graph5");
    cogsBreakdownGraph(graphData.cogs_breakdown, "graph6");
    productWiseReveneueGraph(graphData.productwise_revenue, "graph7");
  },
  error: function(error_data) {
    console.log("Error");
    console.log(error_data);
  }
})

function salesPerformanceGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var chartdata = data.chartdata;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: labels,
        datasets: [{
            label: chartLabel,
            data: chartdata,
            backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
        },
        options: {
        scales: {
            yAxes: [{
            ticks: {
                beginAtZero: true
            }
            }]
        }
        }
    });
}

function profitLossGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
            label: data.dataset[0].label,
            backgroundColor: "#3e95cd",
            data: data.dataset[0].profitData
          }, {
            label: data.dataset[1].label,
            backgroundColor: "#8e5ea2",
            data: data.dataset[1].lossData
          }]
      },
      options: {
        title: {
            display: true,
            text: chartLabel
        }
      }
    });
}

function inflowOutflowGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
            label: data.dataset[0].label,
            backgroundColor: "#3e95cd",
            data: data.dataset[0].inflowData
          }, {
            label: data.dataset[1].label,
            backgroundColor: "#8e5ea2",
            data: data.dataset[1].outflowData
          }]
      },
      options: {
        title: {
            display: true,
            text: chartLabel
        }
      }
    });
}

function runwayGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var chartdata = data.chartdata;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
              label: chartLabel,
              backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
              data: chartdata
            }]
        },
        options: {
          title: {
              display: true,
              text: "Let's check"
          }
        }
    });
}

function cogsBreakdownGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var chartdata = data.chartdata;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
              label: chartLabel,
              backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
              data: chartdata
            }]
        },
        options: {
          title: {
              display: true,
              text: "Let's check"
          }
        }
    });
}

function productWiseReveneueGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel;
    var ctx = document.getElementById(id).getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
            label: data.dataset[0].label,
            backgroundColor: "#3e95cd",
            data: data.dataset[0].aData
          }, {
            label: data.dataset[1].label,
            backgroundColor: "#8e5ea2",
            data: data.dataset[1].bData
          }]
      },
      options: {
        indexAxis: 'y',
        title: {
            display: true,
            text: chartLabel
        }
      }
    });
}