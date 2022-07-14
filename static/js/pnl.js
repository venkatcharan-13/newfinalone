const endpoint = 'api/pnlData/';
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
    fillPnlTableIncome(response.income.data, 'income');
    fillPnlTableCogs(response.cost_of_goods_sold, 'cogs', 'Costs of Goods Sold');
    fillPnlTableExpenses(response.expense, 'expense');
    fillPnlTableTotals(response.income, 'income_total', 'Income');
    fillPnlTableTotals(response.total_expense, 'expense_total', 'Expenses');
    fillPnlTableIndividuals(response.gross_profit, 'grossprofit', 'Gross Profit');
    fillPnlTableIndividuals(response.ebitda, 'ebitda', 'EBITDA');
    fillPnlTableIndividuals(response.depreciation_expenses, 'dep_exp', 'Depreciation Expenses');
    fillPnlTableIndividuals(response.pbit, 'pbit', 'PBIT');
    fillPnlTableIndividuals(response.interest_expenses, 'int_exp', 'Interest Expenses');
    fillPnlTableIndividuals(response.pbt, 'pbt', 'PBT');
    document.getElementById('head_sales').innerHTML = response.total_income.current;
    document.getElementById('head_grossprofit').innerHTML = response.gross_profit.current;
    document.getElementById('head_cogs').innerHTML = response.cost_of_goods_sold.current ? response.cost_of_goods_sold.current : 0;
    document.getElementById('head_exp').innerHTML = response.total_expense.current;
    document.getElementById('head_profit').innerHTML = response.pbt.current;
  },
  error: function (error_data) {
    console.log("Error1");
    console.log(error_data);
  }
})

function changePeriod(params) {
  sessionStorage.setItem("choosen_month", params);
  location.reload();
}

function fillPnlTableTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
}

function fillPnlTableIncome(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td style="width:35%;"> <a href="' + 'pnl/' + object.account_header + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
      '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
      '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
      '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
      '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
    table.appendChild(tr);
  })
}

function fillPnlTableCogs(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 8%;text-align: center;">' + '' + '</td>' +
    '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 8%; text-align: center;">' + '' + '</td>' +
    '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
}


function fillPnlTableIndividuals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 8%;text-align: center;">' + object.curr_per + '%</td>' +
    '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 8%; text-align: center;">' + object.prev_per + '%</td>' +
    '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
}

function fillPnlTableExpenses(data, tid) {
  var table = document.getElementById(tid);
  Object.keys(data).forEach(function (category) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:35%">' + category + '</th>' +
    '<th style="width: 12%; text-align:right;">' + data[category]['current'] + '</th>' +
    '<th style="width: 8%;text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:right;">' + data[category]['previous'] + '</th>' +
    '<th style="width: 8%; text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:center;">' + data[category]['per_change'] + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + data[category]['three_month_avg'] + '</th>';
    table.appendChild(tr)
    data[category]['data'].forEach(function (object) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td style="width:35%;"> <a href="' + 'pnl/' + object.account_header + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
        '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
        '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
        '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
        '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
        '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
        '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
      table.appendChild(tr);
    })
  })
}