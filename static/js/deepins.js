const endpoint = 'api/deepinsData/';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function (data) {
    console.log("Success Deep Insights");
    fillDeepInsightOne(data.deep_insight_one, "deep_insight_one");
    fillDeepInsightTwo(data.deep_insight_two, "deep_insight_two");
    document.getElementById("deep_insight_three").innerHTML = data.deep_insight_three;
    fillDeepInsightFour(data.deep_insight_four, "deep_insight_four");
    fillDeepInsightFive(data.deep_insight_five, "deep_insight_five");
    fillDeepInsightSix(data.deep_insight_six, "deep_insight_six");
    fillDeepInsightSeventoNine(data.deep_insight_seven, "deep_insight_seven");
    fillDeepInsightSeventoNine(data.deep_insight_eight, "deep_insight_eight");
    fillDeepInsightSeventoNine(data.deep_insight_nine, "deep_insight_nine");
    fillDeepInsightTen(data.deep_insight_ten, "deep_insight_ten");
    document.getElementById("deep_insight_eleven").innerHTML = data.deep_insight_eleven;
    fillDeepInsightTweleve(data.deep_insight_twelve, "deep_insight_twelve");
  },
  error: function (error_data) {
    console.log("Error Deep Insights");
    console.log(error_data);
  }
})

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
  console.log(data);
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
  console.log(data);
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