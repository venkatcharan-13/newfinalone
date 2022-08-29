const endpoint = 'api/deepinsData/';
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
    console.log("Success Deep Insights");
    fillDeepInsightOne(response.deep_insight_one, "deep_insight_one");
    fillDeepInsightTwo(response.deep_insight_two, "deep_insight_two");
    document.getElementById("deep_insight_three").innerHTML = response.deep_insight_three;
    fillDeepInsightFour(response.deep_insight_four, "deep_insight_four");
    fillDeepInsightFive(response.deep_insight_five, "deep_insight_five");
    fillDeepInsightSix(response.deep_insight_six, "deep_insight_six");
    fillDeepInsightSeventoNine(response.deep_insight_seven, "deep_insight_seven");
    fillDeepInsightSeventoNine(response.deep_insight_eight, "deep_insight_eight");
    fillDeepInsightSeventoNine(response.deep_insight_nine, "deep_insight_nine");
    fillDeepInsightTen(response.deep_insight_ten, "deep_insight_ten");
    document.getElementById("deep_insight_eleven").innerHTML = response.deep_insight_eleven;
    fillDeepInsightTweleve(response.deep_insight_twelve, "deep_insight_twelve");
  },
  error: function (error_data) {
    console.log("Error Deep Insights");
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

function fillDeepInsightOne(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_name + '</td>' +
    '<td>' + object.payee + '</td>' +
    '<td>' + object.date + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightTwo(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_name + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightFour(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_header + '</td>' +
    '<td>' + object.current + '</td>' +
    '<td>' + object.previous + '</td>' +
    '<td>' + object.per_change + '%</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightFive(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_name + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightSix(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_name + '</td>' +
    '<td>' + object.payee + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightSeventoNine(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.payee + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}

function fillDeepInsightTen(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var li = document.createElement('li');
    li.innerHTML = object;
    table.appendChild(li);
  })
}

function fillDeepInsightTweleve(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + object.account_name + '</td>' +
    '<td>' + object.payee + '</td>' +
    '<td>' + object.date + '</td>' +
    '<td>' + object.amount + '</td>';
    table.appendChild(tr);
  })
}