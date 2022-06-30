const endpoint = 'api/balsheetData';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    console.log("Success Balance Sheet");
    fillBalsheetRows(data.cash, 'cash');
    fillBalsheetRows(data.bank, 'bank');
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
    document.getElementById('head_equity').innerHTML = data.total_equity;
    document.getElementById('head_liabilities').innerHTML = data.total_liabilities;
    document.getElementById('head_assets').innerHTML = data.total_assets;
  },
  error: function (error_data) {
    console.log("Error2");
    console.log(error_data);
  }
})

function fillBalsheetRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.account_header + '</th>' +
      '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
    table.appendChild(tr);
  })
}