const endpoint = 'api/insightsData/';
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
    console.log("Success Insights");
    fillExpenseHeader(response.response_data.advt_and_marketing_header, "advt_and_marketing", "Advertising and Marketing Expenses");
    fillExpenseHeader(response.response_data.employement_header, "employement", "Employment Expenses");
    fillExpenseHeader(response.response_data.rent_rates_and_repairs_header, "rent_rate_repair", "Rent, Rates & Repairs Expenses");
    fillExpenseHeader(response.response_data.brokerage_and_commission_header, "brokerage_commission", "Brokerage & Commission Charges");
    fillExpenseHeader(response.response_data.general_and_admin_header, "general_and_admin", "General & Admin Charges");
    fillInsightsData(response.response_data.advt_and_marketing_insights, "advt_and_marketing_insights");
    fillInsightsData(response.response_data.employement_insights, "employement_insights");
    fillInsightsData(response.response_data.rent_rates_and_repairs_insights, "rent_rate_repair_insights");
    fillInsightsData(response.response_data.brokerage_and_commission_insights, "brokerage_commission_insights");
    fillInsightsData(response.response_data.general_and_admin_insights, "general_and_admin_insights");
    document.getElementById("current_month").innerHTML = response.current_period;
    document.getElementById("previous_month").innerHTML = response.previous_period;
  },
  error: function (error_data) {
    console.log("Error Insights");
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

function fillExpenseHeader(object, tid, head) {
  var rowbtn = `<button type="button" id="rotateBtn" class="accordion-toggle" data-bs-toggle="collapse" data-bs-target=".${tid}" aria-expanded="false" aria-hidden="true"><svg cla xmlns="\http://www.w3.org/2000/svg&quot;" viewBox="0 0 66.91 122.88" focusable="false" ><path d="M1.95,111.2c-2.65,2.72-2.59,7.08,0.14,9.73c2.72,2.65,7.08,2.59,9.73-0.14L64.94,66l-4.93-4.79l4.95,4.8 c2.65-2.74,2.59-7.11-0.15-9.76c-0.08-0.08-0.16-0.15-0.24-0.22L11.81,2.09c-2.65-2.73-7-2.79-9.73-0.14 C-0.64,4.6-0.7,8.95,1.95,11.68l48.46,49.55L1.95,111.2L1.95,111.2L1.95,111.2z"></path></svg></button>`
  document.getElementById(tid).innerHTML = `<th style="width:40%"> <a href="${head}/?selected_date=${choosen_month}" style="text-decoration: none">${head}</a> ${rowbtn} <br><em>Change: ${object.change}</em></th>` +
    '<td style="width: 15%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 15%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 15%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 15%; text-align:right;">' + object.three_month_avg + '</td>';
}


function fillInsightsData(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = `<li> This month we incurred additional expenses amounting to <b>INR ${object.additional}</b>
    for the product/services availed from<b>${object.payee ? object.payee : 'Unknown'}</b></li>`;
    table.appendChild(tr);
  })
}
