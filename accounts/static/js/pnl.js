const endpoint = 'api/pnlData/';
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
  success: function (response) {
    console.log("Success PNL");
    document.getElementById('current_month').innerHTML = response.current_period;
    document.getElementById('previous_month').innerHTML = response.previous_period;
    fillPnlTableIncome(response.response_data.income.data, 'income');
    fillPnlTableCogs(response.response_data.cost_of_goods_sold, 'cogs', 'Costs of Goods Sold');
    fillPnlTableExpenses(response.response_data.expense, 'expense');
    fillPnlTableTotals(response.response_data.income, 'income_total', 'Income');
    fillPnlTableExpenseTotals(response.response_data.total_expense, 'expense_total', 'Expenses');
    fillPnlTableGrossProfit(response.response_data.gross_profit, 'grossprofit', 'Gross Profit');
    fillPnlTableIndividuals(response.response_data.ebit, 'ebit', 'EBIT');
    // fillPnlTableIndividuals(response.response_data.depreciation_expenses, 'dep_exp', 'Depreciation Expenses');
    // fillPnlTableIndividuals(response.response_data.pbit, 'pbit', 'PBIT');
    fillPnlTableIndividuals(response.response_data.interest_expenses, 'int_exp', 'Interest Expenses');
    fillPnlTableIndividuals(response.response_data.tax_expenses, 'tax_exp', 'Taxes');
    fillPnlTableIndividuals(response.response_data.net_profit, 'netprofit', 'Net Profit');
    document.getElementById('head_sales').innerHTML = response.response_data.total_income.current;
    document.getElementById('head_grossprofit').innerHTML = response.response_data.gross_profit.current;
    document.getElementById('head_cogs').innerHTML = response.response_data.cost_of_goods_sold.current ? response.response_data.cost_of_goods_sold.current : 0;
    document.getElementById('head_exp').innerHTML = response.response_data.total_expense.current;
    document.getElementById('head_profit').innerHTML = response.response_data.net_profit.current;
  },
  error: function (error_data) {
    console.log("Error1");
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

function fillPnlTableTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
}

function fillPnlTableExpenseTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + object.curr_per + '%</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + object.prev_per + '%</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
}

function fillPnlTableIncome(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td style="width:35%;"> <a href="pnl/' + object.account_for_coding + '/?selected_date=' + choosen_month + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
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

function fillPnlTableGrossProfit(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + object.curr_per + '%</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + object.prev_per + '%</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
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
    '<th style="width: 8%;text-align: center;">' +  data[category]['curr_per'] + '%</th>' +
    '<th style="width: 12%; text-align:right;">' + data[category]['previous'] + '</th>' +
    '<th style="width: 8%; text-align: center;">' +  data[category]['prev_per'] + '%</th>' +
    '<th style="width: 12%; text-align:center;">' + data[category]['per_change'] + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + data[category]['three_month_avg'] + '</th>';
    table.appendChild(tr)
    data[category]['data'].forEach(function (object) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td style="width:35%;"> <a href="pnl/' + object.account_for_coding + '/?selected_date=' + choosen_month + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
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