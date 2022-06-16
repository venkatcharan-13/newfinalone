function add_actionable_remark(pk) {
    var remark_val = $('#actionRemark' + pk).val();
    $.ajax({
        url: "add_actionable_remark/" + pk + "/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({actionRemark: remark_val}),
        dataType: 'json',
    });
    // $.post("add_remark/" + pk + "/", {
    //     rkey: String(remark_val)
    // },"json");
    document.location.reload();
}

function add_watchout_remark(pk) {
    var remark_val = $('#watchoutRemark' + pk).val();
    $.ajax({
        url: "add_watchout_remark/" + pk + "/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({watchoutRemark: remark_val}),
        dataType: 'json',
    });
    document.location.reload();
}