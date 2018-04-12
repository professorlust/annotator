function screen(button) {
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

    if (start_date > end_date) {
        alert("Start Date > End Date!");
        return
    }

    var formData = new FormData();
    formData.append('start_date', start_date);
    formData.append('end_date', end_date);
    $.ajax({
        type: 'POST',
        url: '/billing',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log("Response received.");
            // var billing_table_title = document.getElementById('billing_table_title');
            // billing_table_title.innerHTML = document.getElementById("start_date").value+'-'+document.getElementById("end_date").value;
            
            var billing_table = document.getElementById('billing_table');
            var td = billing_table.getElementsByTagName("td");

            var i = 0;  //annotator counter
            for(var key in response['annotators']) {
               td[i*3].innerHTML = response['essay_progress'][key];
               td[i*3+1].innerHTML = response['ocr_progress'][key];
               td[i*3+2].innerHTML = response['essay_progress'][key]+response['ocr_progress'][key];
               i++;
            }
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Please check the date format!\n\n' + textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}