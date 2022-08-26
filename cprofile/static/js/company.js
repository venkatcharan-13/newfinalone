const endpoint = 'api/company_info/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
      console.log("Success Company Info");
      fillInputArea(response.name, 'company_name');
      fillInputArea(response.industry, 'industry');
      fillInputArea(response.entity_name, 'entity_name');
      fillInputArea(response.address, 'address');
      fillInputArea(response.city, 'city');
      fillInputArea(response.state, 'state');
      fillInputArea(response.zip, 'zip');
      fillInputArea(response.country, 'country');
      fillInputArea(response.contact_person, 'contact_person');
      fillInputArea(response.email, 'contact_email');
      fillInputArea(response.phone, 'contact_num');
      fillInputArea(response.gst_no, 'gst_no');
      fillInputArea(response.pan_no, 'pan_no');
      fillInputArea(response.pf_no, 'pf_no');
      fillInputArea(response.esic_no, 'esic_no');
    },
    error: function (error_data) {
      console.log("Error");
      console.log(error_data);
    }
  })

  
function fillInputArea(data, id) {
    document.getElementById(id).value = data;
}

function saveCompanyInfo() {
    var edited_name = $('#company_name').val();
    var edited_industry = $('#industry').val();
    var edited_entity = $('#entity_name').val();
    var edited_address = $('#address').val();
    var edited_city = $('#city').val();
    var edited_state = $('#state').val();
    var edited_zip = $('#zip').val();
    var edited_contact_person = $('#contact_person').val();
    var edited_email = $('#contact_email').val();
    var edited_number = $('#contact_num').val();
    var edited_gst_no = $('#gst_no').val();
    var edited_pan_no = $('#pan_no').val();
    var edited_pf_no = $('#pf_no').val();
    var edited_esic_no = $('#esic_no').val();

    $.ajax({
        url: "save_company_info/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            edited_name: edited_name,
            edited_industry: edited_industry,
            edited_entity: edited_entity,
            edited_address: edited_address,
            edited_city: edited_city,
            edited_state: edited_state,
            edited_zip: edited_zip,
            edited_contact_person: edited_contact_person,
            edited_email: edited_email,
            edited_number: edited_number,
            edited_gst_no: edited_gst_no,
            edited_pan_no: edited_pan_no,
            edited_pf_no: edited_pf_no,
            edited_esic_no: edited_esic_no
        }),
        dataType: 'json',
    }).done(function (data) {
        console.log("Info Edited");
        document.location.reload();
    }).fail(function (error) {
        console.log("Edit failed");
    });
}