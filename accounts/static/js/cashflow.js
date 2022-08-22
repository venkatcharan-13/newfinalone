const endpoint = 'api/cashflowData';
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
  document.getElementById(tid).innerHTML = `<th style="width:40%"> ${head} 
    <span class="fa fa-info-circle" title="${info}"></span></th>` +
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