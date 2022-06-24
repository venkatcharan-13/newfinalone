const endpoint = 'api/pnlData/';
const endpoint2 = 'api/balsheetData';
// const accounts_endpoint = endpoint + 'accounts'
// const transactions_endpoint = endpoint + 'transactions'

$.ajax({
  method: "GET",
  url: endpoint,
  success: function(data) {
    console.log("Success");
    fillPnlTableRows(data.income, 'income');
    fillPnlTableRows(data.cost_of_goods_sold, 'cogs');
    fillPnlTableRows(data.expense, 'expense');
    document.getElementById('grossprofit').innerHTML = '<b>' + data.gross_profit + '</b>';
    document.getElementById('ebitda').innerHTML = '<b>' + data.ebitda + '</b>';
  },
  error: function(error_data) {
    console.log("Error");
    console.log(error_data);
  }
})

$.ajax({
  method: "GET",
  url: endpoint2,
  success: function(data) {
    console.log("Success2");
    fillBalsheetRows(data.cash, 'cash');
    fillBalsheetRows(data.accounts_receivable, 'acc_rec');
    fillBalsheetRows(data.fixed_asset, 'fixasset');
    fillBalsheetRows(data.other_current_asset, 'ocasset');
    fillBalsheetRows(data.other_asset, 'othasset');
    fillBalsheetRows(data.stock, 'stock');
    fillBalsheetRows(data.accounts_payable, 'acc_pay');
    fillBalsheetRows(data.long_term_liability, 'ltliab');
    fillBalsheetRows(data.other_current_liability, 'ocliab');
    fillBalsheetRows(data.other_liability, 'othliab');
    fillBalsheetRows(data.equity, 'equity');
  },
  error: function(error_data) {
    console.log("Error");
    console.log(error_data);
  }
})


function fillPnlTableRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.account_header + '</th>' +
    '<td style="width: 13%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 13%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 13%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 21%; text-align:right;">' + object.three_month_avg + '</td>';
    table.appendChild(tr);
  })
}

function fillBalsheetRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.account_header + '</th>' +
    '<td style="width: 13%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 13%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 13%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 21%; text-align:right;">' + object.three_month_avg + '</td>';
    table.appendChild(tr);
  })
}