var endpoint = 'api/incometaxData/';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month"): "2022-06-30";
var choosen_fy = sessionStorage.getItem("choosen_fy") ? sessionStorage.getItem("choosen_fy"): "2022";

$(document).ready(function() {
  if(sessionStorage.getItem("choosen_month")){
    $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
  }
  if(sessionStorage.getItem("choosen_fy")){
    $('#fySelector').val(sessionStorage.getItem("choosen_fy"));
  }
  else{
    $('#fySelector').val("Choose FY");
  }

});

$.ajax({
  method: "GET",
  url: endpoint,
  data: {
    selected_date: choosen_month,
    selected_fy: choosen_fy
  },
  success: function (response) {
    console.log("Income Tax data loaded");
    createAlertBoxes(response.alerts, "alertsBox");
    createRadioElement(response.status.monthly, "monthly_status");
    createRadioElement(response.status.quarterly, "quarterly_status");
  },
  error: function (error_data) {
    console.log("Error");
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

function changeFinYear(params) {
  console.log(params);
  sessionStorage.setItem("choosen_fy", params);
  location.reload();
}


function createAlertBoxes(data, id) {
  var box = document.getElementById(id);
  data.forEach(function (object) {
    var div = document.createElement('div');
    div.innerHTML = '<div class="card">' +
      `<div class="card-body"> <p class="card-text"> ${object.desc} <b> ${object.dueDate} </b></p></div></div><br>`;
    box.appendChild(div);
  })
}

function createRadioElement(data, eid) {
  elem = document.getElementById(eid);
  Object.entries(data).forEach(function (month) {
    var div = document.createElement('div');
    div.className = "form-check col-3";
    switch (month[1]) {
      case "done":
        var color = "green";
        break;
      case "action_required":
        var color = "red";
        break;
      case "quality_check":
        var color = "blue";
        break;
      default:
        var color = "white";
        break;
    }
    div.innerHTML = `<input class="form-check-input" type="radio" style="background-color: ${color}" checked>` +
      `<label class="form-check-label" for="flexRadioDefault1">${month[0]}</label>`;

    elem.appendChild(div, elem.nextSibling);
  })
}