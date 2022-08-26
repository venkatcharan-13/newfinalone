var endpoint = 'api/incometaxData/';
var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month") : "2022-06-30";
var choosen_fy = sessionStorage.getItem("choosen_fy") ? sessionStorage.getItem("choosen_fy") : "2022";

$(document).ready(function () {
  if (sessionStorage.getItem("choosen_month")) {
    $('#periodSelector').val(sessionStorage.getItem("choosen_month").substring(0, 7));
  }
  if (sessionStorage.getItem("choosen_fy")) {
    $('#fySelector').val(sessionStorage.getItem("choosen_fy"));
  }
  else {
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
    fillMonthlyTaxStatus(response.status.monthly, "monthly_status");
    fillQuarterlyTaxStatus(response.status.quarterly, "quarterly_status");
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
    div.innerHTML = '<div class="card w-50">' +
      `<div class="card-body"> <p class="card-text"> ${object.desc} <b> ${object.dueDate} </b></p></div></div><br>`;
    box.appendChild(div);
  })
}

function showPending(params) {
  for (var i = 0; i < document.getElementsByClassName(params).length; i++) {
    document.getElementsByClassName(params)[i].style.display = 'none';
  }
}

function showAll(params) {
  for (var i = 0; i < document.getElementsByClassName(params).length; i++) {
    document.getElementsByClassName(params)[i].setAttribute('style', 'display:flex;align-items:center;justify-content:center;');
  }
}

function fillMonthlyTaxStatus(data, eid) {
  elem = document.getElementById(eid);
  var icon = '';
  Object.entries(data).forEach(function (month) {
    var div = document.createElement('div');
    div.setAttribute('style', 'display:flex; align-items:center; justify-content:center;');
    div.setAttribute('class', 'col-2 shadow-sm monthlyStatus');
    switch (month[1]) {
      case "done":
        icon = `<i class="fi fi-rs-check"></i>`;
        break;
      case "action_required":
        icon = `<i class="fi fi-rs-sensor-alert"></i>`;
        break;
      case "not_applicable":
        icon = `<i class="fi fi-rs-lock"></i>`;
        break;
      default:
        div.setAttribute('class', 'col-2 shadow-sm');
        icon = `<i class="fi fi-rs-hourglass-end"></i>`;
        break;
    }
    div.innerHTML = icon +
      `<label class="fa" for="flexRadioDefault1">${month[0]}</label>`;

    elem.appendChild(div, elem.nextSibling);
  })
}

function fillQuarterlyTaxStatus(data, eid) {
  elem = document.getElementById(eid);
  var icon = '';
  Object.entries(data).forEach(function (month) {
    var div = document.createElement('div');
    div.setAttribute('style', 'display:flex; align-items:center; justify-content:center;');
    div.setAttribute('class', 'col-3 shadow-sm quarterlyStatus');
    switch (month[1]) {
      case "done":
        icon = `<i class="fi fi-rs-check"></i>`;
        break;
      case "action_required":
        icon = `<i class="i fi-rs-sensor-alert"></i>`;
        break;
      case "not_applicable":
        icon = `<i class="fi fi-rs-lock"></i>`;
        break;
      default:
        div.setAttribute('class', 'col-3 shadow-sm');
        icon = `<i class="fi fi-rs-hourglass-end"></i>`;
        break;
    }
    div.innerHTML = icon +
      `<label class="fa" for="flexRadioDefault1">${month[0]}</label>`;

    elem.appendChild(div, elem.nextSibling);
  })
}