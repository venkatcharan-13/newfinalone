function updateFromZoho(clientId) {
    $.ajax({
        url: "/admin/updatezoho/" + clientId + "/",
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({clientId: clientId}),
        // dataType: 'json',
    }).done(function (data) {
        console.log("Made an API call from admin");
        document.location.reload();
    }).fail(function (error) {
        console.log("Error making API call");
    });
}