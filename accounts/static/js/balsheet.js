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
    document.getElementById("current_month").innerHTML = response.current_period;
    document.getElementById("previous_month").innerHTML = response.previous_period;
    fillTotalHead(response.response_data.total_assets, 'total_of_assets', 'Assets');
    fillBalsheetHeads(response.response_data.fixed_asset, 'Fixed Asset', 'fixasset_head');
    addBalsheetRows(response.response_data.fixed_asset.data, 'fixasset_head', 'asset_type');
    fillBalsheetHeads(response.response_data.other_asset, 'Other Asset', 'othasset_head');
    addBalsheetRows(response.response_data.other_asset.data, 'othasset_head', 'asset_type');
    fillSingleBalsheetRow(response.response_data.accounts_receivable[0], 'acc_rec');
    fillSingleBalsheetRow(response.response_data.bank[0], 'bank');
    fillSingleBalsheetRow(response.response_data.cash[0], 'cash');
    fillBalsheetHeads(response.response_data.other_current_asset, 'Other Current Asset', 'ocasset_head');
    addBalsheetRows(response.response_data.other_current_asset.data, 'ocasset_head', 'asset_type');
    fillBalsheetHeads(response.response_data.stock, 'Stock', 'stock_head');
    addBalsheetRows(response.response_data.stock.data, 'stock_head', 'asset_type');

    fillTotalHead(response.response_data.total_liabilities, 'total_of_liabilities', 'Liabilities');
    fillBalsheetHeads(response.response_data.long_term_liability, 'Long Term Liability', 'ltliab_head');
    addBalsheetRows(response.response_data.long_term_liability.data, 'ltliab_head', 'liability_type');
    fillBalsheetHeads(response.response_data.other_liability, 'Other Liability', 'othliab_head')
    addBalsheetRows(response.response_data.other_liability.data, 'othliab_head', 'liability_type');
    fillSingleBalsheetRow(response.response_data.accounts_payable[0], 'acc_pay');
    fillBalsheetHeads(response.response_data.other_current_liability, 'Other Current Liability', 'ocliab_head');
    addBalsheetRows(response.response_data.other_current_liability.data, 'ocliab_head', 'liability_type');

    fillTotalHead(response.response_data.total_equity, 'total_of_equity', 'Equity');
    addBalsheetRows(response.response_data.equity.data, 'equity', 'equity_type');

    document.getElementById('head_equity').innerHTML = response.response_data.total_equity.current;
    document.getElementById('head_liabilities').innerHTML = response.response_data.total_liabilities.current;
    document.getElementById('head_assets').innerHTML = response.response_data.total_assets.current;  
    document.getElementById('table_info').innerHTML = response.description;
    document.getElementById('table_info_head').innerHTML = "Balance Sheet";
    displayClientNotes(response.client_notes, 'clientNotesBlock');
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
  tr.innerHTML = '<th style="width:34%">' + head + '</th>' +
    '<th style="width: 22%; text-align:right;">' + data.current_total + '</th>' +
    '<th style="width: 22%; text-align:right;">' + data.previous_total + '</th>' +
    '<th style="width: 22%; text-align:center;">' + data.overall_change + '%</th>';
}


function fillSingleBalsheetRow(data, rid){
  var tr = document.getElementById(rid);
  tr.innerHTML = '<th style="width:34%">' + data.account_header + '</th>' +
    '<td style="width: 22%; text-align:right;">' + data.current + '</td>' +
    '<td style="width: 22%; text-align:right;">' + data.previous + '</td>' +
    '<td style="width: 22%; text-align:center;">' + data.per_change + '%</td>';
}

function addBalsheetRows(data, rid, rowType) {
  var table = document.getElementById('balsheet_table');
  var i = document.getElementById(rid).rowIndex + 1;

  data.forEach(function (object) {
    var tr = table.insertRow(i);
    if(rowType == 'asset_type'){
      tr.setAttribute('class', 'accordion-collapse collapse assetsHiddenRows');
    } else if (rowType == 'liability_type') {
      tr.setAttribute('class', 'accordion-collapse collapse liabilitiesHiddenRows');
    } else {
      tr.setAttribute('class', 'accordion-collapse collapse equityHiddenRows');
    }
    tr.innerHTML = '<th style="width:34%">' + object.account_header + '</th>' +
      '<td style="width: 22%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 22%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 22%; text-align:center;">' + object.per_change + '%</td>';
    i++;
  })
}

function fillTotalHead(data, tid, head) {
  var tr = document.getElementById(tid);
  tr.innerHTML = '<th style="width:34%">' + head + '</th>' +
    '<th style="width: 22%; text-align:right;">' + data.current + '</th>' +
    '<th style="width: 22%; text-align:right;">' + data.previous + '</th>' +
    '<th style="width: 22%; text-align:center;">' + data.per_change + '%</th>';
}

function displayClientNotes(notes, id) {
  var box = document.getElementById(id);
  notes.forEach(function (note) {
    var div = document.createElement('div');
    div.setAttribute('class', 'card mb-2');
    div.innerHTML = `<div class="card-header"> <small> ${note.created_on} </small></div>` + 
    `<div class="card-body"> <p class="card-text"> ${note.note}</p>` +
    `<footer class="blockquote-footer">Response: ${note.admin_response == null ? '': note.admin_response}</footer> </div>`;
    box.appendChild(div);
  })
}


function add_client_note() {
  var written_note = $('#newNote').val();
  console.log(written_note);
  $.ajax({
      url: "/accounts/add_client_note/",
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({
        note: written_note,
        period: choosen_month,
        table: 'balsheet'
      }),
      dataType: 'json',
  }).done(function (data) {
      console.log("Success");
      document.location.reload();
  }).fail(function (error) {
      console.log("error");
  });
}