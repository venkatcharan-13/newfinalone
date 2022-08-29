const endpoint = 'api/bank_details/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
        console.log("Success Bank");
        displayBankDetails(response);
    },
    error: function (error_data) {
        console.log("Error");
        console.log(error_data);
    }
})

var bankCounter = 0, newBanksCounter = 0;

function displayBankDetails(data) {
    data.forEach(object => {
        bankCounter ++;
        var htmlOfCard = `
            <div class="accordion-item shadow-sm border-light my-3">
            <h2 class="accordion-header" id="headingOne">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#bank_count_${bankCounter}" aria-expanded="true" >
            <b>${object.bank_name}</b>
            </button>
            </h2>
            <div id="bank_count_${bankCounter}" class="accordion-collapse collapse" >
            <div class="accordion-body">
            <div class="row">
                <div class="col-6">
                    <div>
                        <label for="bank_name" class="mb-1 fw-bold">Bank Name</label>
                        <input type="text" class="form-control mb-3" id="bank_name_${bankCounter}" value="${object.bank_name}">
                    </div>
                </div>
                <div class="col-6">
                    <div>
                        <label for="acc_num" class="mb-1 fw-bold">Account No</label>
                        <input type="text" class="form-control mb-3" id="acc_num_${bankCounter}" value="${object.account_number}">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-6">
                    <div>
                        <label for="ifsc_code" class="mb-1 fw-bold">IFSC Code</label>
                        <input type="text" class="form-control " id="ifsc_${bankCounter}" value="${object.ifsc_code}">
                    </div>
                </div>
                <div class="col-6">
                    <div>
                        <label for="branch_location" class="mb-1 fw-bold">Branch Location</label>
                        <input type="text" class="form-control " id="branch_${bankCounter}" value="${object.location}">
                    </div>
                </div>
            </div>
            </div>
            </div>
            </div>
            `;

        document.getElementById('bankDetailsList').insertAdjacentHTML('beforeend', htmlOfCard)
    });
}

function addNewBank() {
    newBanksCounter ++;
    var htmlOfCard = `
        <div class="accordion-item shadow-sm border-light my-3">
        <h2 class="accordion-header" id="headingOne">
        <button class="accordion-button " type="button" data-bs-toggle="collapse" data-bs-target="#bank_count_${bankCounter + newBanksCounter}" aria-expanded="true" >
        New Bank Account Details
        </button>
        </h2>
        <div id="bank_count_${bankCounter + newBanksCounter}" class="accordion-collapse collapse show" >
        <div class="accordion-body">
        <div class="row">
            <div class="col-6">
                <div>
                    <label for="bank_name" class="mb-1 fw-bold">Bank Name</label>
                    <input type="text" class="form-control mb-3" id="bank_name_${bankCounter + newBanksCounter}">
                </div>
            </div>
            <div class="col-6">
                <div>
                    <label for="acc_num" class="mb-1 fw-bold">Account No</label>
                    <input type="text" class="form-control mb-3" id="acc_num_${bankCounter + newBanksCounter}">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
                <div>
                    <label for="ifsc_code" class="mb-1 fw-bold">IFSC Code</label>
                    <input type="text" class="form-control " id="ifsc_${bankCounter + newBanksCounter}">
                </div>
            </div>
            <div class="col-6">
                <div>
                    <label for="branch_location" class="mb-1 fw-bold">Branch Location</label>
                    <input type="text" class="form-control " id="branch_${bankCounter + newBanksCounter}">
                </div>
            </div>
        </div>
        </div>
        </div>
        </div>`;
    document.getElementById('bankDetailsList').insertAdjacentHTML('beforeend', htmlOfCard)
}


function saveBankDetails() {
    var newBanksAdded = [];
    for (let i = 1; i <= bankCounter + newBanksCounter; i++) {
        newBanksAdded.push({
            bank_name: document.getElementById('bank_name_' + i).value,
            bank_acc_num: document.getElementById('acc_num_' + i).value,
            bank_ifsc_code: document.getElementById('ifsc_' + i).value,
            bank_branch: document.getElementById('branch_' + i).value
        })
    }

    $.ajax({
        url: "save_bank_details/",
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(newBanksAdded),
        dataType: 'json',
        success: function (data) {
            console.log("Bank Details added");
            document.location.reload();
        },
        error: function (error) {
            console.log(error);
        }
    });
}