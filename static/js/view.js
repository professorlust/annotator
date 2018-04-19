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

    var annotator = document.getElementById("annotator").value;

    var formData = new FormData();
    formData.append('start_date', start_date);
    formData.append('end_date', end_date);
    formData.append('annotator', annotator);
    $.ajax({
        type: 'POST',
        url: '/view ',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log("Response received.");

            var start_timestamp = response['start_timestamp'];
            var end_timestamp = response['end_timestamp'];
            var essay_record_length = response['essay_record_length']
            var ocr_record_length = response['ocr_record_length']
            var annotator_valid_flag = response['annotator_valid_flag'];

            if (start_timestamp > end_timestamp) {
                alert("Start Date > End Date!");
                return
            }

            if (!annotator_valid_flag){
                alert("Annotator not valid!");
                return
            }

            clean_screen_record();

            if (essay_record_length > ocr_record_length){
                for(i=0;i<ocr_record_length;i++){
                    var tr = document.createElement("tr");
                    var td_essay_record = document.createElement("td");
                    var td_ocr_record = document.createElement("td");
                    td_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'][i],null, 4);
                    td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'][i],null, 4);
                    tr.appendChild(td_essay_record);
                    tr.appendChild(td_ocr_record);
                    record_area.appendChild(tr);
                }
                for(i=ocr_record_length;i<essay_record_length;i++){
                    var tr = document.createElement("tr");
                    var td_essay_record = document.createElement("td");
                    var td_ocr_record = document.createElement("td");
                    td_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'][i],null, 4);
                    td_ocr_record.innerHTML = "";
                    tr.appendChild(td_essay_record);
                    tr.appendChild(td_ocr_record);
                    record_area.appendChild(tr);
                }
            }
            else{
                if(essay_record_length < ocr_record_length){
                    for(i=0;i<essay_record_length;i++){
                        var tr = document.createElement("tr");
                        var td_essay_record = document.createElement("td");
                        var td_ocr_record = document.createElement("td");
                        td_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'][i],null, 4);
                        td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'][i],null, 4);
                        tr.appendChild(td_essay_record);
                        tr.appendChild(td_ocr_record);
                        record_area.appendChild(tr);
                    }
                    for(i=essay_record_length;i<ocr_record_length;i++){
                        var tr = document.createElement("tr");
                        var td_essay_record = document.createElement("td");
                        var td_ocr_record = document.createElement("td");
                        td_essay_record.innerHTML = "";
                        td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'][i],null, 4);;
                        tr.appendChild(td_essay_record);
                        tr.appendChild(td_ocr_record);
                        record_area.appendChild(tr);
                    }
                }
                else{
                    for(i=0;i<essay_record_length;i++){
                        var tr = document.createElement("tr");
                        var td_essay_record = document.createElement("td");
                        var td_ocr_record = document.createElement("td");
                        td_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'][i],null, 4);
                        td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'][i],null, 4);
                        tr.appendChild(td_essay_record);
                        tr.appendChild(td_ocr_record);
                        record_area.appendChild(tr);
                    }
                }
            }

            // if (essay_record_length == 0){
            //     screen_essay_record.innerHTML = 'null';
            // }
            // else{
            //     screen_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'],null, 4);
            // }
            // if (ocr_record_length == 0){
            //     screen_ocr_record.innerHTML = 'null';
            // }
            // else{
            //     screen_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'],null, 4);
            // }
            
            // var tr = document.createElement("tr");
            // var td_essay_record = document.createElement("td");
            // var td_ocr_record = document.createElement("td");

            // if (essay_record_length == 0){
            //     td_essay_record.innerHTML = 'null';
            // }
            // else{
            //     td_essay_record.innerHTML = JSON.stringify(response['screen_essay_record'],null, 4);
            // }
            // if (ocr_record_length == 0){
            //     td_ocr_record.innerHTML = 'null';
            // }
            // else{
            //     td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'],null, 4);
            // }
            
            // tr.appendChild(td_essay_record);
            // tr.appendChild(td_ocr_record);
            // god_view_table.appendChild(tr);

            
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Please check the date format!\n\n' + textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}
function clean_screen_record(){
    var record_area = document.getElementById('record_area');
    var tr = record_area.getElementsByTagName("tr");
    var len = tr.length;
    for(i=len-1;i>=0;i--){
        tr[i].parentNode.removeChild(tr[i]);
    }
}