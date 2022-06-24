/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    rowObject = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    // console.log('Format wala');
    // console.log(d.subcategory);
    d.subcategory.forEach(element => {
        rowObject += '<tr> <td style="padding-left:50px;"> ' + element.header + '</td><td style="padding-left:150px;"> ' + element.current + '</td> <td style="padding-left:150px;">' + element.previous + '</td> <td style="padding-left:150px;">' + element.three_month_avg + '</td></tr>';
    });
    
    rowObject += '</table>';
    return (
        rowObject
    );
}

$(document).ready(function () {
    var table;

    // Add event listener for opening and closing details
    $('#example').on('click', 'tbody td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
        } else {
            // Open this row
            row.child(format(row.data())).show();
        }
    });

    $('#example').on('requestChild.dt', function (e, row) {
        row.child(format(row.data())).show();
    });


    $.ajax({
        method: "GET",
        url: 'api/zohoData/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (resData) {
            console.log("Success");
            table = $('#example').DataTable({
                ajax: '../static/obj2.txt',
                rowId: 'id',
                stateSave: true,
                columns: [
                    {
                        className: 'dt-control',
                        orderable: false,
                        data: null,
                        defaultContent: '',
                    },
                    { data: 'category' },
                    '',
                    '',
                    '',
                ],
                order: [[1, 'asc']],
            });
        },
        error: function (error_data) {
            console.log("Error");
            console.log(error_data);
        }
    })

});