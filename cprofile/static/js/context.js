const endpoint = 'api/context_data/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
        console.log("Success Context");
        fill_input_area(response.about, 'about_company');
        fill_input_area(response.work_profile, 'work_profile');
        fill_input_area(response.key_info, 'key_info');
        fill_input_area(response.specific_request, 'specific_request');
        new FroalaEditor('textarea');
    },
    error: function (error_data) {
        console.log("Error");
        console.log(error_data);
    }
})


function fill_input_area(data, id) {
    document.getElementById(id).value = data;
}

function save_context() {
    var edited_about = $('#about_company').val();
    var edited_work_profile = $('#work_profile').val();
    var edited_key_info = $('#key_info').val();
    var edited_specific_request = $('#specific_request').val();
    $.ajax({
        url: "save_company_context/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            edited_about: edited_about,
            edited_work_profile: edited_work_profile,
            edited_key_info: edited_key_info,
            edited_specific_request: edited_specific_request
        }),
        dataType: 'json',
    }).done(function (data) {
        console.log("Info Edited");
        document.location.reload();
    }).fail(function (error) {
        console.log("Edit failed");
    });
}