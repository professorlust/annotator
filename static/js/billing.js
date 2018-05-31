function screen(button) {
    var start_time = document.getElementById("start_time").value;
    if (start_time == "") {
        alert("Please enter the Start Time!");
        return
    }

    var end_time = document.getElementById("end_time").value;
    if (end_time == "") {
        alert("Please enter the End Time!");
        return
    }

    var formData = new FormData();
    formData.append('start_time', start_time);
    formData.append('end_time', end_time);
    $.ajax({
        type: 'POST',
        url: '/billing',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log("Response received.");

            var start_timestamp = response['start_timestamp'];
            var end_timestamp = response['end_timestamp'];

            if (start_timestamp > end_timestamp) {
                alert("Start Time > End Time!");
                return
            }

            var billing_table = document.getElementById('billing_table');
            var td = billing_table.getElementsByTagName("td");

            var i = 0;  //annotator counter
            for(var key in response['annotators']) {
               td[i*3].innerHTML = response['essay_progress'][key];
               td[i*3+1].innerHTML = response['ocr_progress'][key];
               td[i*3+2].innerHTML = response['ocr_char_count'][key];
               td[i*3+3].innerHTML = response['essay_progress'][key] + response['ocr_progress'][key];
               i++;
            }
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Please check the time format!\n\n' + textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}