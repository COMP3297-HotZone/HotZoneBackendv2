
var cluster_list;

function selectCluster(){
    var select = document.getElementById( 'clusters' );
    if(select.value){
        var table = $('#clusterTable').DataTable();
        table.clear();
        locIndex = select.value - 1
        locationCase = cluster_list['cluster'][locIndex]
        $.each(locationCase, function(i, val) {
            table.row.add([val.x,val.y,val.day,val.caseNo,val.locationName]).draw( false );
        })
    }
};

function getCluster(){
    $.ajax({
        type: "GET",
        dataType: "json",
        data: {'d': $('#D').val(),'t': $('#T').val(),'c':$('#C').val()},
        url: "../cluster_get/",
        success: function(result) {
            cluster_list = JSON.parse(result);
            console.log(cluster_list);
           
            var select = document.getElementById('clusters');
            for(i = select.options.length-1; i >= 0; i--) {
                  select.remove(i);
            }
            for ( i = 1; i <= cluster_list['Total clusters']; i += 1 ) {
                option = document.createElement( 'option' );
                option.value = i;
                option.text = `Cluster #${i}`
                select.add( option );
            }
            if(cluster_list['Total clusters']==0){
                alert("No Cluster Yet");
            }
           
        
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    })
};

$(document).ready(function() {
    getCluster();
    var table = $('#clusterTable').DataTable(
        {
            "scrollY":        "500px",
            "scrollCollapse": true,
            "paging":         false,
            "searching": false,
            "aaSorting": [],
            "ordering": false,
            "columnDefs": [
                {"className": "dt-center", "targets": "_all"}
            ]
        }
    );
});