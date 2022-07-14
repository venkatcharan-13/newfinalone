const endpoint = 'api/cashflowData';
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
    console.log("Success Cashflow");
    fillCashflowTotals(response.beginning_cash_balance, 'beg_cash_bal', 'Beginning Cash Balance');
    fillCashflowRows(response.cashflow_from_operating_activities, 'cashflowA');
    fillCashflowTotals(response.net_cash_a, 'netA', 'Cashflow from Operations');
    fillCashflowRows(response.cashflow_from_investing_activities, 'cashflowB');
    fillCashflowTotals(response.net_cash_b, 'netB', 'Cashflow from Investing');
    fillCashflowRows(response.cashflow_from_financing_activities, 'cashflowC');
    fillCashflowTotals(response.net_cash_c, 'netC', 'Cashflow from Financing');
    fillCashflowTotals(response.net_change_abc, 'netABC', 'Net Change in Cash (A)+(B)+(C)');
    fillCashflowTotals(response.ending_cash_balance, 'endbal', 'Ending Cash Balance');
  },
  error: function (error_data) {
    console.log("Error3");
    console.log(error_data);
  }
})

function changePeriod(params) {
  sessionStorage.setItem("choosen_month", params);
  location.reload();
}

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