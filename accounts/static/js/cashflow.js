const endpoint = 'api/cashflowData';
var choosen_month = sessionStorage.getItem("choosen_month") ? 
sessionStorage.getItem("choosen_month"): new Date().toISOString().slice(0, 10);

$(document).ready(function() {
  if(sessionStorage.getItem("choosen_month")){
    $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
  }
  else{
    $('#periodSelector').val(choosen_month.slice(0, 7));
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
    document.getElementById("current_month").innerHTML = response.current_period;
    document.getElementById("previous_month").innerHTML = response.previous_period;
    fillCashflowTotals(response.response_data.beginning_cash_balance, 'beg_cash_bal', 'Beginning Cash Balance');
    fillCashflowRows(response.response_data.cashflow_from_operating_activities, 'cf_op_head');
    fillCashflowHeaders(response.response_data.net_cash_a, 'cf_op_head', 'A. Cash Flow from Operating Activities', response.cashflow_A_info);
    fillCashflowRows(response.response_data.cashflow_from_investing_activities, 'cf_inv_head');
    fillCashflowHeaders(response.response_data.net_cash_b, 'cf_inv_head', 'B. Cash Flow from Investing Activities', response.cashflow_B_info);
    fillCashflowRows(response.response_data.cashflow_from_financing_activities, 'cf_fin_head');
    fillCashflowHeaders(response.response_data.net_cash_c, 'cf_fin_head', 'C. Cash Flow from Financing Activities', response.cashflow_C_info);
    fillCashflowTotals(response.response_data.net_change_abc, 'netABC', 'Net Change in Cash (A)+(B)+(C)');
    fillCashflowTotals(response.response_data.ending_cash_balance, 'endbal', 'Ending Cash Balance');
    document.getElementById('head_cf_operations').innerHTML = response.response_data.net_cash_a.current;
    document.getElementById('head_cf_investing').innerHTML = response.response_data.net_cash_b.current;
    document.getElementById('head_cf_financing').innerHTML = response.response_data.net_cash_c.current;
    document.getElementById('head_cash_bal').innerHTML = response.response_data.beginning_cash_balance.current;
    document.getElementById('table_info').innerHTML = response.description;
    document.getElementById('table_info_head').innerHTML = "Cashflow";
    displayClientNotes(response.client_notes, 'clientNotesBlock');
  },
  error: function (error_data) {
    console.log("Error3");
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

function fillCashflowRows(data, rid, rowType) {
  var table = document.getElementById('cashflow_table');
  var i = document.getElementById(rid).rowIndex + 1;
  if(data.length == 0){
    var tr = table.insertRow(i);
    tr.innerHTML = '<td></td>';
  }
  data.forEach(function (object) {
    if (object.activity == "Net Income" || object.activity == "Plus: Depreciation and Amortization"){
      var href = '#';
    }else{
      var href = `${object.activity}/?selected_date=${choosen_month}`;
    }
    var tr = table.insertRow(i);
    tr.setAttribute('class', `accordion-collapse collapse ${rid}`);
    tr.innerHTML = `<th style="width:40%"><a href="${href}" 
    style="text-decoration: none">${object.activity}</a></th>` +
      '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
    i++;
  })
}

function fillCashflowHeaders(object, tid, head, info) {
  var expandButton = `<button type="button" id="rotateBtn" class="accordion-toggle" data-bs-toggle="collapse" data-bs-target=".${tid}" aria-expanded="false" aria-hidden="true"><svg cla xmlns="\http://www.w3.org/2000/svg&quot;" viewBox="0 0 66.91 122.88" focusable="false" ><path d="M1.95,111.2c-2.65,2.72-2.59,7.08,0.14,9.73c2.72,2.65,7.08,2.59,9.73-0.14L64.94,66l-4.93-4.79l4.95,4.8 c2.65-2.74,2.59-7.11-0.15-9.76c-0.08-0.08-0.16-0.15-0.24-0.22L11.81,2.09c-2.65-2.73-7-2.79-9.73-0.14 C-0.64,4.6-0.7,8.95,1.95,11.68l48.46,49.55L1.95,111.2L1.95,111.2L1.95,111.2z"></path></svg></button>`;
  document.getElementById(tid).innerHTML = `<th style="width:40%"> ${head} 
    <span class="fa fa-info-circle" title="${info}"></span> ${expandButton} </th>` + 
    '<th style="width: 20%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 20%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 20%; text-align:center;">' + object.per_change + '%</th>';
}

function fillCashflowTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:40%">' + head + '</th>' +
    '<th style="width: 20%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 20%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 20%; text-align:center;">' + object.per_change + '%</th>';
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
        table: 'cashflow'
      }),
      dataType: 'json',
  }).done(function (data) {
      console.log("Success");
      document.location.reload();
  }).fail(function (error) {
      console.log("error");
  });
}