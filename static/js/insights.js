const endpoint = 'api/insightsData/';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    console.log("Success Insights");
    fillExpenseHeader(data.advt_and_marketing_header, "advt_and_marketing", "Advertising and Marketing Expenses");
    fillExpenseHeader(data.employement_header, "employement", "Employment Expenses");
    fillExpenseHeader(data.rent_rates_and_repairs_header, "rent_rate_repair", "Rent, Rates & Repairs Expenses");
    fillExpenseHeader(data.brokerage_and_commission_header, "brokerage_commission", "Brokerage & Commission Charges");
    fillExpenseHeader(data.general_and_admin_header, "general_and_admin", "General & Admin Charges");
    fillInsightsData(data.advt_and_marketing_insights, "advt_and_marketing_insights");
    fillInsightsData(data.employement_insights, "employement_insights");
    fillInsightsData(data.rent_rates_and_repairs_insights, "rent_rate_repair_insights");
    fillInsightsData(data.brokerage_and_commission_insights, "brokerage_commission_insights");
    fillInsightsData(data.general_and_admin_insights, "general_and_admin_insights");
  },
  error: function (error_data) {
    console.log("Error Insights");
    console.log(error_data);
  }
})

function fillExpenseHeader(object, tid, head) {
  console.log(object);
  document.getElementById(tid).innerHTML = '<th style="width:40%">' + head + '<br><em>Change: ' + object.change + '</em></th>' +
    '<td style="width: 15%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 15%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 15%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 15%; text-align:right;">' + object.three_month_avg + '</td>';
}


function fillInsightsData(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<li> This month Additional amount of ' + object.additional + ' is paid to<b>' + (object.payee ? object.payee : 'Unknown') + '</b></li>';
    table.appendChild(tr);
  })
}
