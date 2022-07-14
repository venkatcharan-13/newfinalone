const endpoint = 'api/ratiosData/';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month"): "2022-06-30";

$(document).ready(function() {
    if(sessionStorage.getItem("choosen_month")){
      $('#periodSelector').val(sessionStorage.getItem("choosen_month"));
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
    success: function (response) {
        console.log("Success PNL");
        fillRatiosHead(response.gross_profit, 'gross_profit', 'Gross Profit');
        fillRatiosHead(response.pbt, 'pbt', 'PBT');
        fillRatiosTableRows(response.profit_ratios, 'profit_ratios');
        fillRatiosTableRows(response.liquidity_ratio, 'liquidity_ratio');
        fillRatiosTableRows(response.op_eff_ratios, 'op_eff_ratios');
        fillRatiosTableRows(response.solvency_ratios, 'solvency_ratios');
    },
    error: function (error_data) {
        console.log("Error4");
        console.log(error_data);
    }
})

function changePeriod(params) {
    sessionStorage.setItem("choosen_month", params);
    location.reload();
}

function fillRatiosHead(object, tid, head) {
    document.getElementById(tid).innerHTML = '<th style="width:40%">' + head + '</th>' +
        '<td style="width: 10%; text-align:right;">' + object.current + '</td>' +
        '<td style="width: 10%; text-align:right;">' + object.previous + '</td>' +
        '<td style="width: 20%; text-align:center;">' + object.three_month_avg + '</td>' +
        '<td style="width: 20%; text-align:center;"></td>';
}


function fillRatiosTableRows(data, tid) {
    var table = document.getElementById(tid);
    data.forEach(function (object) {
        var tr = document.createElement('tr');
        tr.innerHTML = '<th style="width:40%">' + object.ratio_head + '</th>' +
            '<td style="width: 10%; text-align:right;">' + object.current + '</td>' +
            '<td style="width: 10%; text-align:right;">' + object.previous + '</td>' +
            '<td style="width: 20%; text-align:center;">' + object.three_month_avg + '</td>' +
            '<td style="width: 20%; text-align:center;"></td>';
        table.appendChild(tr);
    })
}
