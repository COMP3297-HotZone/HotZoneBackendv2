var retrievedResult, table;

$(document).ready(function() {
    $('#caseRecordTable tfoot th').each(function() {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search' + title + '" />');
    });
    retrieveAllCaseRecord();
});

function retrieveAllCaseRecord() {
    $.ajax({
        type: "GET",
        dataType: "json",
        crossDomain: true,
        url: "../all_caserecord_get/",
        success: function(result) {
            console.log(result);
            retrievedResult = JSON.parse(result);
            // $("#retrieveStatus").text("Retrieved Success!");
            updateResult();
            // $('#confirmButton').attr("disabled", false);
            if (result.resultCode == 200) {
                alert("SUCCESS");
            };
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
            // $("#locationRadio").text("");
            // $("#retrieveStatus").text("Retrieved Falied!");
        }
    })
}

function updateResult() {
    // $.each(retrievedResult, function(i, val) {
    //     table.row.add([val.id, val.patient.name, val.patient.dateOfBirth, val.virus.name, val.localOrImported]).draw(false);;
    // });
    $('#caseRecordTable').DataTable({
        data: retrievedResult,
        columnDefs: [{
                targets: [0, 1, 2, 3, 4],
                className: 'dt-head-left'
            },
            {
                targets: 5,
                className: 'dt-body-center'
            },
            { orderable: false, targets: [4, 5] }
        ],
        columns: [
            { data: 'id' },
            { data: 'patient.name' },
            { data: 'patient.dateOfBirth' },
            { data: 'virus.name' },
            { data: 'localOrImported' },
            {
                data: 'id',
                render: function(data, type) {
                    return '<a href="' + data + '">View Location Records</a>'
                }
            }

        ],
        initComplete: function() {
            this.api().columns().every(function() {
                var that = this;

                $('input', this.footer()).on('keyup change clear', function() {
                    if (that.search() !== this.value) {
                        that.search(this.value)
                            .draw();
                    }
                });
            });
            var f = document.getElementsByTagName("tfoot");
            for (var i = 0; i < f.length; i++) {
                f[i].style.display = "table-row-group";
            };
        }
    });
}