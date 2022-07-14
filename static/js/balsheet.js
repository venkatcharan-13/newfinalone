const endpoint = 'api/balsheetData';
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
    console.log("Success Balance Sheet");
    fillBalsheetRows(response.cash, 'cash');
    fillBalsheetRows(response.bank, 'bank');
    fillBalsheetRows(response.accounts_receivable, 'acc_rec');
    fillBalsheetRows(response.fixed_asset, 'fixasset');
    fillBalsheetRows(response.other_current_asset, 'ocasset');
    fillBalsheetRows(response.other_asset, 'othasset');
    fillBalsheetRows(response.stock, 'stock');
    fillBalsheetRows(response.accounts_payable, 'acc_pay');
    fillBalsheetRows(response.long_term_liability, 'ltliab');
    fillBalsheetRows(response.other_current_liability, 'ocliab');
    fillBalsheetRows(response.other_liability, 'othliab');
    fillBalsheetRows(response.equity, 'equity');
    document.getElementById('head_equity').innerHTML = response.total_equity;
    document.getElementById('head_liabilities').innerHTML = response.total_liabilities;
    document.getElementById('head_assets').innerHTML = response.total_assets;
  },
  error: function (error_data) {
    console.log("Error2");
    console.log(error_data);
  }
})

function changePeriod(params) {
  sessionStorage.setItem("choosen_month", params);
  location.reload();
}

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