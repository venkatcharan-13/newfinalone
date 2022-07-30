var endpoint = 'api/reportData/';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month"): "2022-06-30";

$(document).ready(function() {
  if(sessionStorage.getItem("choosen_month")){
    $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
  }
  else{
    $('#periodSelector').val("Choose Month");
  }
});

$.ajax({
  method: "GET",
  url: endpoint,
  data: {
    selected_date: choosen_month
  },
  success: function (graphData) {
    console.log("Graph data loaded");
    salesPerformanceGraph(graphData.monthly_sales_performance, "sales_performance1");
    salesPerformanceGraph(graphData.quarterly_sales_performance, "sales_performance2");
    salesPerformanceGraph(graphData.yearly_sales_performance, "sales_performance3");
    incomeExpensesGraph(graphData.income_vs_expenses, "income_vs_expenses");
    incomeExpensesGraph(graphData.cash_inflow_outflow, "inflow_vs_outflow");
    salesPerformanceGraph(graphData.closing_bank_balance_trend, "closing_bank_balance");
    grossAndNetProfitGraph(graphData.gross_and_net_profit, "gross_and_net_profit");
    runwayGraph(graphData.runaway, "monthly_runaway");
    gpExpensesEbitdaGraph(graphData.gp_vs_expenses_vs_ebitda, "gp_expenses_ebitda");
    showSixMonthSummary(graphData.pnl_summary, "pnl_head", "pnl_summary");
    showSixMonthSummary(graphData.bal_sheet_summary, "bal_sheet_head", "bal_sheet_summary");
    showSixMonthSummary(graphData.cashflow_summary, "cashflow_head", "cashflow_summary");
    montlhyCashFlowGraph(graphData.monthly_cashflow, "monthly_cashflow");
  },
  error: function (error_data) {
    console.log("Error");
    console.log(error_data);
  }
})

function changePeriod(params) {
  console.log(params);
  var year = params.substring(0, 4);
  var month = params.substring(5, 7);
  var choosen_period = params + '-' + new Date(year, month, 0).getDate(); 
  sessionStorage.setItem("choosen_month", choosen_period);
  location.reload();
}

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
      locale: 'en-IN',
      scales: {
        y: [{
          beginAtZero: true
          // ticks: {
          //   callback: (value) => {
          //     return new Intl.NumberFormat('en-IN', {
          //       style: 'currency',
          //       currency: 'INR',
          //     }).format(value)
          //   }
          // }
        }]
      }
    }
  });
}

function incomeExpensesGraph(data, id) {
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
        data: data.dataset[0].profitData,
        borderSkipped: false
      }, {
        label: data.dataset[1].label,
        backgroundColor: "#8e5ea2",
        data: data.dataset[1].lossData,
        borderSkipped: false
      }],
    },
    options: {
      locale: 'en-IN',
      title: {
        display: true,
        text: chartLabel
      },
      scales: {
        x: {
          stacked: true,
          position: 'top'
        },
        y: {
          beginAtZero: true
        }
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
      locale: 'en-IN',
      title: {
        display: true,
        text: chartLabel
      }
    }
  });
}


function grossAndNetProfitGraph(data, id) {
  var labels = data.labels;
  var chartLabel = data.chartLabel;
  var dataset = data.dataset;
  var ctx = document.getElementById(id).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: dataset[0].label,
        backgroundColor: "#3e95cd",
        data: dataset[0].grossProfitValues
      },
      {
        label: dataset[1].label,
        backgroundColor: "#8e5ea2",
        data: dataset[1].netProfitValues
      }],
    },
  })
}

function runwayGraph(data, id) {
  var labels = data.labels;
  var chartLabel = data.chartLabel;
  var chartdata = data.chartdata;
  var ctx = document.getElementById(id).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: chartLabel,
        backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", "#8e5ea2"],
        data: chartdata
      }]
    },
  });
}

function gpExpensesEbitdaGraph(data, id) {
  var labels = data.labels;
  var chartLabel = data.chartLabel;
  var ctx = document.getElementById(id).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        type: 'bar',
        label: data.dataset[0].label,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        data: data.dataset[0].data
      }, {
        type: 'bar',
        label: data.dataset[1].label,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        data: data.dataset[1].data
      }, {
        type: 'line',
        label: data.dataset[2].label,
        backgroundColor: "#3e95cd",
        data: data.dataset[2].data,
        yAxisID: 'percentage'
      }
      ]
    },
    options: {
      locale: 'en-IN',
      barPercentage: 1,
      title: {
        display: true,
        text: chartLabel
      },
      scales: {
        y: {
          beginAtZero: true,
          position: 'left'
        },
        percentage: {
          beginAtZero: true,
          position: 'right',
          grid: {
            drawOnChartArea: false
          }
        }
      }
    }
  });
}

function montlhyCashFlowGraph(data, id) {
  var labels = data.labels;
  var chartLabel = data.chartLabel;
  var dataset = data.dataset;
  var ctx = document.getElementById(id).getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: dataset[0].label,
        backgroundColor: "#3e95cd",
        borderColor:  "#3e95cd",
        data: dataset[0].cashflowOperations
      },
      {
        label: dataset[1].label,
        backgroundColor: "#8e5ea2",
        borderColor: "#8e5ea2",
        data: dataset[1].cashflowInvesting
      },
      {
        label: dataset[2].label,
        backgroundColor: "#00a300",
        borderColor:  "#00a300",
        data: dataset[2].cashflowFinancing
      }],
    },
    options: {
      locale: 'en-IN',
    }
  })
}

function showSixMonthSummary(data, id, tid) {
  document.getElementById(id).innerHTML = '<thead><th style="width:40%;"> Month </th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[0] + '</th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[1] + '</th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[2] + '</th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[3] + '</th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[4] + '</th>' +
    '<th style="width: 10%; text-align:right;">' + data.months[5] + '</th></thead>';
  var table = document.getElementById(tid);
  Object.keys(data).forEach(function (category) {
    if (category == 'months')
      return;
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%;">' + category + '</th>' +
      '<td style="width: 10%; text-align:right;">' + data[category][0] + '</td>' +
      '<td style="width: 10%; text-align:right;">' + data[category][1] + '</td>' +
      '<td style="width: 10%; text-align:right;">' + data[category][2] + '</td>' +
      '<td style="width: 10%; text-align:right;">' + data[category][3] + '</td>' +
      '<td style="width: 10%; text-align:right;">' + data[category][4] + '</td>' +
      '<td style="width: 10%; text-align:right;">' + data[category][5] + '</td>';
    table.appendChild(tr);
  })
}