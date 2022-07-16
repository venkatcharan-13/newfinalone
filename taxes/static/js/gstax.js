var endpoint = 'api/gstData/';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (response) {
    console.log("GST data loaded");
    createAlertBoxes(response.alerts, "alertsBox");
    createRadioElement(response.status.monthly, "monthly_status");
    createRadioElement(response.status.quarterly, "quarterly_status");
  },
  error: function (error_data) {
    console.log("Error");
    console.log(error_data);
  }
})

function createAlertBoxes(data, id) {
  var box = document.getElementById(id);
  data.forEach(function (object) {
    var div = document.createElement('div');
    div.innerHTML = '<div class="card">' +
      `<div class="card-body"> <p class="card-text"> ${object.desc} <b> ${object.dueDate} </b></p>` +
      `<small> ${object.raisedOn} </small></div></div><br>`;
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