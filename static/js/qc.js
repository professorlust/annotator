function qc(button) {
    var start_date = document.getElementById("start_date").value;
    if (start_date == "") {
        alert("Please enter the Start Date!");
        return
    }

    var end_date = document.getElementById("end_date").value;
    if (end_date == "") {
        alert("Please enter the End Date!");
        return
    }

    var formData = new FormData();
    formData.append('start_date', start_date);
    formData.append('end_date', end_date);
    $.ajax({
        type: 'POST',
        url: '/qc',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log("Response received.");

            var start_timestamp = response['start_timestamp'];
            var end_timestamp = response['end_timestamp'];

            if (start_timestamp > end_timestamp) {
                alert("Start Date > End Date!");
                return
            }

            var qc_table = document.getElementById('qc_table');
            var td = billing_table.getElementsByTagName("td");
            td[0].innerHTML = response['qwk'];
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}