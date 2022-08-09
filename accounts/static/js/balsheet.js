const endpoint = 'api/balsheetData';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month") : "2022-06-30";

$(document).ready(function () {
  if (sessionStorage.getItem("choosen_month")) {
    $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
  }
  else {
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
    document.getElementById("current_month_assets").innerHTML = response.current_period;
    document.getElementById("previous_month_assets").innerHTML = response.previous_period;
    document.getElementById("current_month_liabilities").innerHTML = response.current_period;
    document.getElementById("previous_month_liabilities").innerHTML = response.previous_period;
    document.getElementById("current_month_equity").innerHTML = response.current_period;
    document.getElementById("previous_month_equity").innerHTML = response.previous_period;
    fillBalsheetRows(response.response_data.cash, 'cash');
    fillBalsheetRows(response.response_data.bank, 'bank');
    fillBalsheetRows(response.response_data.accounts_receivable, 'acc_rec');
    fillBalsheetHeads(response.response_data.fixed_asset, 'Fixed Asset', 'fixasset_head');
    fillBalsheetRows(response.response_data.fixed_asset.data, 'fixasset');
    fillBalsheetHeads(response.response_data.other_current_asset, 'Other Current Asset', 'ocasset_head');
    fillBalsheetRows(response.response_data.other_current_asset.data, 'ocasset');
    fillBalsheetHeads(response.response_data.other_asset, 'Other Asset', 'othasset_head');
    fillBalsheetRows(response.response_data.other_asset.data, 'othasset');
    fillBalsheetHeads(response.response_data.stock, 'Stock', 'stock_head');
    fillBalsheetRows(response.response_data.stock.data, 'stock');
    fillBalsheetRows(response.response_data.accounts_payable, 'acc_pay');
    fillBalsheetHeads(response.response_data.long_term_liability, 'Long Term Liability', 'ltliab_head');
    fillBalsheetRows(response.response_data.long_term_liability.data, 'ltliab');
    fillBalsheetHeads(response.response_data.other_current_liability, 'Other Current Liability', 'ocliab_head');
    fillBalsheetRows(response.response_data.other_current_liability.data, 'ocliab');
    fillBalsheetHeads(response.response_data.other_liability, 'Other Liability', 'othliab_head')
    fillBalsheetRows(response.response_data.other_liability.data, 'othliab');
    fillBalsheetRows(response.response_data.equity, 'equity');
    document.getElementById('head_equity').innerHTML = response.response_data.total_equity.current;
    document.getElementById('head_liabilities').innerHTML = response.response_data.total_liabilities.current;
    document.getElementById('head_assets').innerHTML = response.response_data.total_assets.current;
    fillTotalHead(response.response_data.total_assets, 'total_of_assets', 'Total Assets');
    fillTotalHead(response.response_data.total_liabilities, 'total_of_liabilities', 'Total Liabilities');
    fillTotalHead(response.response_data.total_equity, 'total_of_equity', 'Total Equity');
  },
  error: function (error_data) {
    console.log("Error2");
    console.log(error_data);
  }
})

function changePeriod(params) {
  var year = params.substring(0, 4);
  var month = params.substring(5, 7);
  var choosen_period = params + '-' + new Date(year, month, 0).getDate();
  sessionStorage.setItem("choosen_month", choosen_period);
  location.reload();
}

function fillBalsheetHeads(data, head, rid){
  var tr = document.getElementById(rid);
  tr.innerHTML = '<th style="width:40%">' + head + '</th>' +
    '<th style="width: 20%; text-align:right;">' + data.current_total + '</th>' +
    '<th style="width: 20%; text-align:right;">' + data.previous_total + '</th>' +
    '<th style="width: 20%; text-align:center;">' + data.overall_change + '%</th>';
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

function fillTotalHead(data, tid, head) {
  var tr = document.getElementById(tid);
  tr.innerHTML = '<th style="width:40%">' + head + '</th>' +
    '<th style="width: 20%; text-align:right;">' + data.current + '</th>' +
    '<th style="width: 20%; text-align:right;">' + data.previous + '</th>' +
    '<th style="width: 20%; text-align:center;">' + data.per_change + '%</th>';
}