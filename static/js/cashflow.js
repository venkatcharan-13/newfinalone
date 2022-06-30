const endpoint = 'api/cashflowData';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    console.log("Success Cashflow");
    fillCashflowTotals(data.beginning_cash_balance, 'beg_cash_bal', 'Beginning Cash Balance');
    fillCashflowRows(data.cashflow_from_operating_activities, 'cashflowA');
    fillCashflowTotals(data.net_cash_a, 'netA', 'Cashflow from Operations');
    fillCashflowRows(data.cashflow_from_investing_activities, 'cashflowB');
    fillCashflowTotals(data.net_cash_b, 'netB', 'Cashflow from Investing');
    fillCashflowRows(data.cashflow_from_financing_activities, 'cashflowC');
    fillCashflowTotals(data.net_cash_c, 'netC', 'Cashflow from Financing');
    fillCashflowTotals(data.net_change_abc, 'netABC', 'Net Change in Cash (A)+(B)+(C)');
    fillCashflowTotals(data.ending_cash_balance, 'endbal', 'Ending Cash Balance');
  },
  error: function (error_data) {
    console.log("Error3");
    console.log(error_data);
  }
})


function fillCashflowRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.activity + '</th>' +
      '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
    table.appendChild(tr);
  })
}

function fillCashflowTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:40%">' + head + '</th>' +
    '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
}