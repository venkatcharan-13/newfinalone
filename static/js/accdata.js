const endpoint = 'api/zohoData/';
const accounts_endpoint = endpoint + 'accounts'
const transactions_endpoint = endpoint + 'transactions'

$.ajax({
  method: "GET",
  url: endpoint,
  success: function(data) {
    console.log("Success");
  },
  error: function(error_data) {
    console.log("Error");
    console.log(error_data);
  }
})