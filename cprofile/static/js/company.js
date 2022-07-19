const endpoint = 'api/company_info/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
      console.log("Success Company Info");
      fill_input_area(response.name, 'company_name');
      fill_input_area(response.industry, 'industry');
      fill_input_area(response.address, 'address');
      fill_input_area(response.city, 'city');
      fill_input_area(response.state, 'state');
      fill_input_area(response.zip, 'zip');
      fill_input_area(response.country, 'country');
      fill_input_area(response.email, 'contact_email');
      fill_input_area(response.phone, 'contact_num');
      fill_input_area(response.gst_no, 'gst_no');
      fill_input_area(response.pan_no, 'pan_no');
      fill_input_area(response.pf_no, 'pf_no');
      fill_input_area(response.esic_no, 'esic_no');
    },
    error: function (error_data) {
      console.log("Error");
      console.log(error_data);
    }
  })

  
function fill_input_area(data, id) {
    document.getElementById(id).value = data;
}

function save_company_info() {
    var edited_name = $('#company_name').val();
    var edited_industry = $('#industry').val();
    var edited_address = $('#address').val();
    var edited_city = $('#city').val();
    var edited_state = $('#state').val();
    var edited_zip = $('#zip').val();
    var edited_email = $('#contact_email').val();
    var edited_number = $('#contact_num').val();
    $.ajax({
        url: "save_company_info/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            edited_name: edited_name,
            edited_industry: edited_industry,
            edited_address: edited_address,
            edited_city: edited_city,
            edited_state: edited_state,
            edited_zip: edited_zip,
            edited_email: edited_email,
            edited_number: edited_number
        }),
        dataType: 'json',
    }).done(function (data) {
        console.log("Info Edited");
        document.location.reload();
    }).fail(function (error) {
        console.log("Edit failed");
    });
}