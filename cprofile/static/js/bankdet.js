const endpoint = 'api/bank_details/'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function (response) {
        console.log("Success Bank");
        show_bank_details(response);
    },
    error: function (error_data) {
        console.log("Error");
        console.log(error_data);
    }
})


function show_bank_details(data) {
    var bank_counter = 1;
    data.forEach(object => {
        if(bank_counter == 1){
            var side_label = `<a class="nav-link active" id="v-pills-bank_${bank_counter}-tab" data-toggle="pill" href="#v-pills-bank_${bank_counter}" role="tab" aria-controls="v-pills-bank_${bank_counter}" aria-selected="true">Bank ${bank_counter}</a>`;
        }
        else{
            var side_label = `<a class="nav-link " id="v-pills-bank_${bank_counter}-tab" data-toggle="pill" href="#v-pills-bank_${bank_counter}" role="tab" aria-controls="v-pills-bank_${bank_counter}" aria-selected="true">Bank ${bank_counter}</a>`
        }
        var bank_detail = `<div class="tab-pane fade show active" id="v-pills-bank_${bank_counter}" role="tabpanel" aria-labelledby="v-pills-bank_${bank_counter}-tab"><label><h6>Bank ${bank_counter} </h6></label>
        <table class="inside_table">
            <tbody>
                <tr>
                    <td>Bank Name</td>
                    <td><input type="text" value="${object.bank_name}" id="bank_name_${bank_counter}"></td>
                </tr>
                <tr>
                    <td>Account No</td>
                    <td><input type="number"  value="${object.account_number}" id="acc_num_${bank_counter}"></td>
                </tr>
                <tr>
                    <td>IFSC Code</td>
                    <td><input type="text" value="${object.ifsc_code}"  id="ifsc_${bank_counter}"></td>
                </tr>
                <tr>
                    <td>Branch Location</td>
                    <td><input type="text" value="${object.location}" id="branch_${bank_counter}"></td>
                </tr>
            </tbody>
        </table></div>`;
        document.getElementById('v-pills-tab').insertAdjacentHTML('beforeend', side_label);
        document.getElementById('v-pills-tabContent').insertAdjacentHTML('beforeend', bank_detail);
        bank_counter++;
    });
}