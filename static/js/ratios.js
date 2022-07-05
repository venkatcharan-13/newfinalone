const endpoint = 'api/ratiosData/';

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (data) {
        console.log("Success PNL");
        fillRatiosHead(data.gross_profit, 'gross_profit', 'Gross Profit');
        fillRatiosHead(data.pbt, 'pbt', 'PBT');
        fillRatiosTableRows(data.profit_ratios, 'profit_ratios');
        fillRatiosTableRows(data.liquidity_ratio, 'liquidity_ratio');
        fillRatiosTableRows(data.op_eff_ratios, 'op_eff_ratios');
        fillRatiosTableRows(data.solvency_ratios, 'solvency_ratios');
    },
    error: function (error_data) {
        console.log("Error4");
        console.log(error_data);
    }
})

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
