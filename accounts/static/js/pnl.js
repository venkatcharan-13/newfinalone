const endpoint = 'api/pnlData/';
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
    console.log("Success PNL");
    document.getElementById('current_month').innerHTML = response.current_period;
    document.getElementById('previous_month').innerHTML = response.previous_period;
    fillPnlTableTotals(response.response_data.income, 'income_total', 'Income');
    fillPnlTableIncome(response.response_data.income.data);
    fillPnlTableCogs(response.response_data.cost_of_goods_sold, 'cogs', 'Costs of Goods Sold');
    fillPnlTableGrossProfit(response.response_data.gross_profit, 'grossprofit', 'Gross Profit');
    fillPnlTableExpenseTotals(response.response_data.total_expense, 'expense_total', 'Expenses');
    fillPnlTableExpenses(response.response_data.expense, 'expense');
    fillPnlTableIndividuals(response.response_data.ebit, 'ebit', 'EBIT');
    fillPnlTableIndividuals(response.response_data.interest_expenses, 'int_exp', 'Interest Expenses');
    fillPnlTableIndividuals(response.response_data.tax_expenses, 'tax_exp', 'Taxes');
    fillPnlTableIndividuals(response.response_data.net_profit, 'netprofit', 'Net Profit');
    document.getElementById('head_sales').innerHTML = response.response_data.total_income.current;
    document.getElementById('head_grossprofit').innerHTML = response.response_data.gross_profit.current;
    document.getElementById('head_cogs').innerHTML = response.response_data.cost_of_goods_sold.current ? response.response_data.cost_of_goods_sold.current : 0;
    document.getElementById('head_exp').innerHTML = response.response_data.total_expense.current;
    document.getElementById('head_profit').innerHTML = response.response_data.net_profit.current;
    document.getElementById('table_info').innerHTML = response.description;
    document.getElementById('table_info_head').innerHTML = "Income Statement";
    displayClientNotes(response.client_notes, 'clientNotesBlock');
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
  var expandButton = '<button type="button" id="rotateBtn" class="accordion-toggle" data-bs-toggle="collapse" data-bs-target=".incomeHiddenRows" aria-expanded="false" aria-hidden="true"><svg cla xmlns="\http://www.w3.org/2000/svg&quot;" viewBox="0 0 66.91 122.88" focusable="false" ><path d="M1.95,111.2c-2.65,2.72-2.59,7.08,0.14,9.73c2.72,2.65,7.08,2.59,9.73-0.14L64.94,66l-4.93-4.79l4.95,4.8 c2.65-2.74,2.59-7.11-0.15-9.76c-0.08-0.08-0.16-0.15-0.24-0.22L11.81,2.09c-2.65-2.73-7-2.79-9.73-0.14 C-0.64,4.6-0.7,8.95,1.95,11.68l48.46,49.55L1.95,111.2L1.95,111.2L1.95,111.2z"></path></svg></button>';
  document.getElementById(tid).innerHTML = '<th style="width:35%">'  + head + expandButton +'</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + '' + '</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
}

function fillPnlTableExpenseTotals(object, tid, head) {
  var expandButton = '<button type="button" id="rotateBtn" class="accordion-toggle" data-bs-toggle="collapse" data-bs-target=".expenseHiddenRows" aria-expanded="false" aria-hidden="true"><svg cla xmlns="\http://www.w3.org/2000/svg&quot;" viewBox="0 0 66.91 122.88" focusable="false" ><path d="M1.95,111.2c-2.65,2.72-2.59,7.08,0.14,9.73c2.72,2.65,7.08,2.59,9.73-0.14L64.94,66l-4.93-4.79l4.95,4.8 c2.65-2.74,2.59-7.11-0.15-9.76c-0.08-0.08-0.16-0.15-0.24-0.22L11.81,2.09c-2.65-2.73-7-2.79-9.73-0.14 C-0.64,4.6-0.7,8.95,1.95,11.68l48.46,49.55L1.95,111.2L1.95,111.2L1.95,111.2z"></path></svg></button>';
  document.getElementById(tid).innerHTML = '<th style="width:35%">' + head + expandButton + '</th>' +
    '<th style="width: 12%; text-align:right;">' + object.current + '</th>' +
    '<th style="width: 8%;text-align: center;">' + object.curr_per + '%</th>' +
    '<th style="width: 12%; text-align:right;">' + object.previous + '</th>' +
    '<th style="width: 8%; text-align: center;">' + object.prev_per + '%</th>' +
    '<th style="width: 12%; text-align:center;">' + object.per_change + '%</th>' +
    '<th style="width: 13%; text-align:right;">' + object.three_month_avg + '</th>';
}

function fillPnlTableIncome(data) {
  var table = document.getElementById('pnltable');
  var i = document.getElementById('income_total').rowIndex + 1;
  if (data.length == 0) {
    var tr = table.insertRow(i);
    tr.innerHTML = '<td></td>';
  }
  data.forEach(function (object) {
    var tr = table.insertRow(i);
    tr.setAttribute('class', 'accordion-collapse collapse incomeHiddenRows');
    tr.innerHTML = '<td style="width:35%;"> <a href="pnl/' + object.account_for_coding + '/?selected_date=' + choosen_month + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
      '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
      '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
      '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
      '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
    i++;
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
  var table = document.getElementById('pnltable');
  var i = document.getElementById('expense_total').rowIndex + 1;
  if (data.length == 0) {
    var tr = table.insertRow(i);
    tr.innerHTML = '<td></td>';
  }
  Object.keys(data).forEach(function (category) {
    var tr = table.insertRow(i);
    tr.innerHTML = '<th style="width:35%">' + category + '</th>' +
      '<th style="width: 12%; text-align:right;">' + data[category]['current'] + '</th>' +
      '<th style="width: 8%;text-align: center;">' + data[category]['curr_per'] + '%</th>' +
      '<th style="width: 12%; text-align:right;">' + data[category]['previous'] + '</th>' +
      '<th style="width: 8%; text-align: center;">' + data[category]['prev_per'] + '%</th>' +
      '<th style="width: 12%; text-align:center;">' + data[category]['per_change'] + '%</th>' +
      '<th style="width: 13%; text-align:right;">' + data[category]['three_month_avg'] + '</th>';
    i++;
    data[category]['data'].forEach(function (object) {
      var tr = table.insertRow(i);
      tr.setAttribute('class', 'accordion-collapse collapse expenseHiddenRows');
      tr.innerHTML = '<td style="width:35%;"> <a href="pnl/' + object.account_for_coding + '/?selected_date=' + choosen_month + '" style="text-decoration: none">' + object.account_header + '</a></td>' +
        '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
        '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
        '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
        '<td style="width: 8%; text-align:right;">' + '' + '</td>' +
        '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
        '<td style="width: 13%; text-align:right;">' + object.three_month_avg + '</td>';
      i++;
    })
  })
}

function displayClientNotes(notes, id) {
  var box = document.getElementById(id);
  notes.forEach(function (note) {
    var div = document.createElement('div');
    div.setAttribute('class', 'card mb-2');
    div.innerHTML = `<div class="card-header"> <small> ${note.created_on} </small></div>` +
      `<div class="card-body"> <p class="card-text"> ${note.note}</p>` +
      `<footer class="blockquote-footer">Response: ${note.admin_response == null ? '' : note.admin_response}</footer> </div>`;
    box.appendChild(div);
  })
}

function add_client_note() {
  var written_note = $('#newNote').val();
  console.log(written_note);
  $.ajax({
    url: "add_client_note/",
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({
      note: written_note,
      period: choosen_month,
      table: 'pnl'
    }),
    dataType: 'json',
  }).done(function (data) {
    console.log("Success");
    document.location.reload();
  }).fail(function (error) {
    console.log("error");
  });
}