const endpoint = 'api/dashboardData/';
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
    console.log("Success Dashboard");
    createNotificationBoxes(response.notifications, "notification_box");
    fillContactCard(response.contact_card, "contact_persons");
    fillDashboardStatus(response.accounts_status, "status_list");
    fillPendingActionables(response.pending_points, "pending_actionables");
    fillWatchoutPoints(response.watchout_points, "watchout_points");
    fillStatutoryCompliances(response.statutory_compliances, "stat_comp");
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

function fillContactCard(data, id) {
  var ul = document.getElementById(id);
  data.forEach(function (object) {
    var li = document.createElement('li');
    li.innerHTML = `${object.name} (${object.profile}) - ${object.number}`;
    ul.appendChild(li);
  })
}


function createNotificationBoxes(data, id) {
  var box = document.getElementById(id);
  data.forEach(function (object) {
    var div = document.createElement('div');
    div.innerHTML = '<div class="card">' +
      `<div class="card-body"> 
      <h6 class="card-title">${object.title}</h6> 
      <p class="card-text"> ${object.content}</p> 
      <small> ${object.days_ago} days ago </small></div></div><br>`;
    box.appendChild(div);
  })
}


function fillPendingActionables(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = `<th> ${object.sno} </th>` +
    `<td> ${object.point} </td>` +
    `<td>
        <div class="input-group">
        <input type="text" class="form-control" value="${object.client_remarks}"
            id="actionRemark${object.id}"></input>
        </div>
    </td>` + 
    `<td>
        <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" 
        ${object.status ? 'checked':''} disabled>
        </div>
    </td>` + 
    `<td>
        <button type="submit" class="btn btn-primary" onClick="add_actionable_remark(${object.id})">
        Add
        </button>
    </td>`;
    table.appendChild(tr);
  })
}

function add_actionable_remark(pk) {
    var remark_val = $('#actionRemark' + pk).val();
    $.ajax({
        url: "add_actionable_remark/" + pk + "/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({actionRemark: remark_val}),
        dataType: 'json',
    }).done(function (data) {
        console.log("Success");
        document.location.reload();
    }).fail(function (error) {
        console.log("error");
    });
}

function fillDashboardStatus(data, tid) {
  var ul = document.getElementById(tid);
  data.forEach(function (object) {
    var li = document.createElement('li');
    if(object.status == "completed"){
      li.className = "list-group-item active";
    } else {
      li.className = "list-group-item"
    }
    li.innerHTML = object.level_desc;
    ul.appendChild(li);
  })
}

function fillWatchoutPoints(data, tid) {
  var list = document.getElementById(tid);
  data.forEach(function (object) {
    var li = document.createElement('li');
    li.className = "list-group-item";
    li.innerHTML = object.point;
    list.appendChild(li);
  })
}

function fillStatutoryCompliances(data, tid) {
  var table = document.getElementById(tid);
  Object.keys(data).forEach(function (tax){
    var tax_head = document.createElement('tr');
    tax_head.innerHTML = `<th scope="row" colspan="5">${tax}</th>`;
    table.appendChild(tax_head);
    data[tax].forEach(function(comp){
      var compliance = document.createElement('tr');
      compliance.innerHTML = `<td scope="row" style="width: 40%;">${comp.compliance}</td>` + 
      `<td style="width: 15%;">${comp.current_month}</td>`;
      table.appendChild(compliance);
    })
  })
}

function copyToClipboard() {
  var copyText = document.getElementById("referralCode");
  navigator.clipboard.writeText(copyText.innerText);
  alert(copyText.innerText)
}
