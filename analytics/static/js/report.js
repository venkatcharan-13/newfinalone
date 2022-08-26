var endpoint = 'api/reportData/';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month") : "2022-06-30";

$(document).ready(function () {
    if (sessionStorage.getItem("choosen_month")) {
        $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
    } else {
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
        simpleBarGraph(graphData.monthly_sales_performance, "sales_performance1")
        simpleBarGraph(graphData.quarterly_sales_performance, "sales_performance2")
        simpleBarGraph(graphData.yearly_sales_performance, "sales_performance3")
        positiveNegativeBarGraph(graphData.income_vs_expenses, "income_vs_expenses");
        positiveNegativeBarGraph(graphData.cash_inflow_outflow, "inflow_vs_outflow");
        simpleBarGraph(graphData.closing_bank_balance_trend, "closing_bank_balance");
        grossAndNetProfitGraph(graphData.gross_and_net_profit, "gross_and_net_profit");
        runwayGraph(graphData.runaway, "monthly_runaway");
        gpExpensesEbitdaGraph(graphData.gp_vs_expenses_vs_ebitda, "gp_expenses_ebitda");
        montlhyCashFlowGraph(graphData.monthly_cashflow, "monthly_cashflow");
        showSixMonthSummary(graphData.pnl_summary, "pnl_head", "pnl_summary");
        showSixMonthSummary(graphData.bal_sheet_summary, "bal_sheet_head", "bal_sheet_summary");
        showSixMonthSummary(graphData.cashflow_summary, "cashflow_head", "cashflow_summary");
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

list_of_graphsHeads = { "monthly": "Monthly Sales Performance", "quaterly": "Quaterly Sales Performance", "yearly": "Yearly Sales Performance" }

function changeGraph(params, bid) {
    list_of_graphs = ['yearly', 'quaterly', 'monthly']
    for (var i = 0; i < 3; i++) {
        if (list_of_graphs[i] == params) {
            document.getElementById(params).style.display = 'block';
        } else {
            document.getElementById(list_of_graphs[i]).style.display = 'none';
        }
    }
}

function simpleBarGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel
    var chartdata = data.chartdata;
    var options = {
        series: [{
            name: chartLabel,
            data: chartdata
        }],
        chart: {
            height: 450,
            type: 'bar',
            toolbar: {
                show: true,
                offsetX: 0,
                offsetY: 0,
                tools: {
                    download: true,
                    selection: true,
                    zoom: true,
                    zoomin: true,
                    zoomout: true,
                    pan: true,
                    reset: true | '<img src="/static/icons/reset.png" width="20">',
                    customIcons: []
                },
                export: {
                    csv: {
                        filename: undefined,
                        columnDelimiter: ',',
                        headerCategory: 'category',
                        headerValue: 'value',
                        dateFormatter(timestamp) {
                            return new Date(timestamp).toDateString()
                        }
                    },
                    svg: {
                        filename: undefined,
                    },
                    png: {
                        filename: undefined,
                    }
                },
                autoSelected: 'zoom'
            },
        },
        plotOptions: {
            bar: {
                borderRadius: 10,
                dataLabels: {
                    position: 'top', // top, center, bottom
                },
            }
        },
        title: {
            text: data.chartLabel,
            align: 'left',
            offsetX: 110
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: '10px',
            },
            formatter: function (val) {
                var novalue = ''
                if (val == '0') {
                    return novalue
                } else {
                    return val.toLocaleString('en-IN');
                }

            },

        },

        xaxis: {
            categories: labels,
            position: 'bottom',
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: '#BED1E6',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
            }
        },

        yaxis: {
            labels: {
                formatter: function (val) {
                    var novalue = ''
                    if (val == '0') {
                        return novalue
                    } else {
                        return val.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
                    }

                },
            },
            axisTicks: {
                show: true,
            },
            axisBorder: {
                show: true,
            },
            tooltip: {
                enabled: true
            },

        }
    };

    var chart = new ApexCharts(document.getElementById(id), options);
    chart.render();
}




function positiveNegativeBarGraph(data, id) {
    var labels = data.labels;
    var options = {
        series: [{
            name: data.dataset[0].label,
            data: data.dataset[0].profitData
        }, {
            name: data.dataset[1].label,
            data: data.dataset[1].lossData
        }],
        chart: {
            type: 'bar',
            height: 450,
            stacked: true,
            toolbar: {
                show: true
            }
        },
        title: {
            text: data.chartLabel,
            align: 'left',
            offsetX: 110
        },
        plotOptions: {
            bar: {
                borderRadius: 5,
                dataLabels: {
                    position: 'top', // top, center, bottom
                },
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                var novalue = ''
                if (val == '0') {
                    return novalue
                } else {
                    return val.toLocaleString('en-IN');;
                }

            }
        },
        xaxis: {
            categories: labels,
            position: 'bottom',
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: '#BED1E6',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
            }

        },
        yaxis: {
            labels: {
                formatter: function (val) {
                    var novalue = ''
                    if (val == '0') {
                        return novalue
                    } else {
                        return val.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
                    }

                },
            }
        }
    };

    var chart = new ApexCharts(document.getElementById(id), options);
    chart.render();


}


function grossAndNetProfitGraph(data, id) {
    var labels = data.labels;
    var options = {
        series: [{
            name: data.dataset[1].label,
            data: data.dataset[1].netProfitValues
        }, {
            name: data.dataset[0].label,
            data: data.dataset[0].grossProfitValues
        },],
        chart: {
            type: 'line',
            height: 450,
            stacked: true
        },
        title: {
            text: data.chartLabel,
            align: 'left',
            offsetX: 110
        },
        plotOptions: {
            bar: {
                borderRadius: 5,
                dataLabels: {
                    position: 'top', // top, center, bottom
                },
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                if (val == '0') {
                    return ''
                } else {
                    return val.toLocaleString('en-IN');;
                }

            }
        },
        xaxis: {
            categories: labels,
            position: 'bottom',
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: '#BED1E6',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
            }

        },
        yaxis: {
            labels: {
                formatter: function (value) {
                    return value + "%";
                }
            },
        }
    };

    var chart = new ApexCharts(document.getElementById(id), options);
    chart.render();
}

function runwayGraph(data, id) {
    var labels = data.labels;
    var chartLabel = data.chartLabel
    var chartdata = data.chartdata;
    var options = {
        series: [{
            name: chartLabel,
            data: chartdata
        }],
        chart: {
            height: 450,
            type: 'line',
        },
        title: {
            text: data.chartLabel,
            align: 'left',
            offsetX: 110
        },
        plotOptions: {
            bar: {

                dataLabels: {
                    position: 'top', // top, center, bottom
                },
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                if (val == '0') {
                    return ''
                } else {
                    return val.toLocaleString('en-IN');;
                }

            },

        },

        xaxis: {
            categories: labels,
            position: 'bottom',
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: 'green',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
            }
        },

    };

    var chart = new ApexCharts(document.getElementById(id), options);
    chart.render();
}


function gpExpensesEbitdaGraph(data, id) {
    var labels = data.labels;
    var options = {
        chart: {
            height: 450,
            type: "line",
            stacked: false,
        },
        dataLabels: {
            enabled: true,
            formatter: function (value) {
                if (value == '0') {
                    return ''
                } else {
                    return value.toLocaleString('en-IN');
                }

            }
        },

        series: [

            {
                name: 'GrossProfit',
                type: 'column',
                data: data.dataset[0].data
            },
            {
                name: "Expenses",
                type: 'column',
                data: data.dataset[1].data
            },
            {
                name: "EBITA",
                type: 'line',
                data: data.dataset[2].data
            },
        ],
        stroke: {
            width: [4, 4, 4]
        },
        plotOptions: {
            bar: {
                columnWidth: "80%"
            }
        },
        xaxis: {
            categories: labels
        },
        yaxis: [{
            seriesName: 'GrossProfit',
            axisTicks: {
                show: true
            },
            axisBorder: {
                show: true,
            },
            title: {
                text: data.dataset[0].label + ' / ' + data.dataset[1].label
            },

            labels: {
                formatter: function (val) {
                    var novalue = ''
                    if (val == '0') {
                        return novalue
                    } else {
                        return val.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
                    }

                },
            },
            tooltip: {
                enabled: true
            }
        },
        {
            seriesName: 'GrossProfit',
            show: false,
            labels: {
                formatter: function (val) {
                    var novalue = ''
                    if (val == '0') {
                        return novalue
                    } else {
                        return val.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
                    }

                },
            },
            tooltip: {
                enabled: true
            }

        }, {
            opposite: true,
            seriesName: 'EBITA',
            axisTicks: {
                show: true
            },
            axisBorder: {
                show: true,
            },
            title: {
                text: data.dataset[2].label
            },

            tooltip: {
                enabled: true
            }

        }
        ],
        tooltip: {
            shared: false,
            intersect: true,
            x: {
                show: false
            }
        },
        legend: {
            horizontalAlign: "center",
            offsetX: 40
        }
    };

    var chart = new ApexCharts(document.getElementById(id), options);

    chart.render();

}


function montlhyCashFlowGraph(data, id) {
    var labels = data.labels;
    var options = {
        series: [{
            name: data.dataset[0].label,
            data: data.dataset[0].cashflowOperations
        }, {
            name: data.dataset[1].label,
            data: data.dataset[1].cashflowInvesting
        }, {
            name: data.dataset[2].label,
            data: data.dataset[2].cashflowFinancing
        }],
        chart: {
            height: 450,
            type: 'line',
        },
        title: {
            text: data.chartLabel,
            align: 'left',
            offsetX: 110
        },
        plotOptions: {
            bar: {
                borderRadius: 10,
                dataLabels: {
                    position: 'top',
                },
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                var novalue = ''
                if (val == '0') {
                    return novalue
                } else {
                    return val.toLocaleString('en-IN', {
                        style: 'currency',
                        currency: 'INR'
                    });
                }

            },

        },

        xaxis: {
            categories: labels,
            position: 'bottom',
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: '#BED1E6',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
            }
        },
        yaxis: {
            labels: {
                formatter: function (val) {
                    var novalue = ''
                    if (val == '0') {
                        return novalue
                    } else {
                        return val.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });
                    }

                },
            }
        }
    };

    var chart = new ApexCharts(document.getElementById(id), options);
    chart.render();
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