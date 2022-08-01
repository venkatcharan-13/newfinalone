const endpoint = 'api/insightsData/';
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
    console.log("Success Insights");
    fillExpenseHeader(response.advt_and_marketing_header, "advt_and_marketing", "Advertising and Marketing Expenses");
    fillExpenseHeader(response.employement_header, "employement", "Employment Expenses");
    fillExpenseHeader(response.rent_rates_and_repairs_header, "rent_rate_repair", "Rent, Rates & Repairs Expenses");
    fillExpenseHeader(response.brokerage_and_commission_header, "brokerage_commission", "Brokerage & Commission Charges");
    fillExpenseHeader(response.general_and_admin_header, "general_and_admin", "General & Admin Charges");
    fillInsightsData(response.advt_and_marketing_insights, "advt_and_marketing_insights");
    fillInsightsData(response.employement_insights, "employement_insights");
    fillInsightsData(response.rent_rates_and_repairs_insights, "rent_rate_repair_insights");
    fillInsightsData(response.brokerage_and_commission_insights, "brokerage_commission_insights");
    fillInsightsData(response.general_and_admin_insights, "general_and_admin_insights");
  },
  error: function (error_data) {
    console.log("Error Insights");
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

function fillExpenseHeader(object, tid, head) {
  document.getElementById(tid).innerHTML = `<th style="width:40%"><a href="${head}/?selected_date=${choosen_month}" style="text-decoration: none">${head}</a><br><em>Change: ${object.change}</em></th>` +
    '<td style="width: 15%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 15%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 15%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 15%; text-align:right;">' + object.three_month_avg + '</td>';
}


function fillInsightsData(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = `<li> This month Additional amount of ${object.additional} is paid to<b> ${object.payee ? object.payee : 'Unknown'} </b></li>`;
    table.appendChild(tr);
  })
}
