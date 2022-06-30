const endpoint = 'api/pnlData/';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    console.log("Success PNL");
    fillPnlTableRows(data.income, 'income');
    fillPnlTableRows(data.cost_of_goods_sold, 'cogs');
    fillPnlTableExpenses(data.expense, 'expense');
    fillPnlTableTotals(data.gross_profit, 'grossprofit', 'Gross Profit');
    fillPnlTableTotals(data.ebitda, 'ebitda', 'EBITDA');
    fillPnlTableTotals(data.depreciation_expenses, 'dep_exp', 'Depreciation Expenses');
    fillPnlTableTotals(data.pbit, 'pbit', 'PBIT');
    fillPnlTableTotals(data.interest_expenses, 'int_exp', 'Interest Expenses');
    fillPnlTableTotals(data.pbt, 'pbt', 'PBT');
    document.getElementById('head_sales').innerHTML = data.total_income.current;
    document.getElementById('head_grossprofit').innerHTML = data.gross_profit.current;
    document.getElementById('head_cogs').innerHTML = data.cost_of_goods_sold.current ? data.cost_of_goods_sold.current : 0;
    document.getElementById('head_exp').innerHTML = data.ebitda.current;
    document.getElementById('head_profit').innerHTML = 'INR 5 lac';
  },
  error: function (error_data) {
    console.log("Error1");
    console.log(error_data);
  }
})

function fillPnlTableRows(data, tid) {
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

function fillPnlTableTotals(object, tid, head) {
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
    tr.innerHTML = '<th>' + category + '</th>';
    table.appendChild(tr)
    data[category].forEach(function (object) {
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