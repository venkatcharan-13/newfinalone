var choosen_month = sessionStorage.getItem("choosen_month") ? sessionStorage.getItem("choosen_month"): "2022-06-30";

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

function changePeriod(params) {
    sessionStorage.setItem("choosen_month", params);
    location.reload();
}