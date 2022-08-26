const endpoint = 'api/overview/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
        console.log("Success Overview");
        fillAddOnSection(response.add_ons_cards, 'addOnsList');
    },
    error: function (error_data) {
        console.log("Error");
        console.log(error_data);
    }
})

function fillAddOnSection(data, did) {
    var div = document.getElementById(did);
    data.forEach(object => {
        var card = document.createElement('div');
        card.setAttribute('class', 'col-6 mb-4');
        card.innerHTML = `<div class="h-100 shadow-sm customCard">
        <div class="customCard-header">
          <h5><b>${object.title}</b></h5>
        </div>
        <div class=" customCard-body">
          <p>${object.content}</p>
        </div>
      </div>`;
      div.append(card);
    })
}