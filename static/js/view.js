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

    var annotators = document.getElementById("annotators");
    var annotator = annotators.options[annotators.selectedIndex].value;

    var formData = new FormData();
    formData.append('start_time', start_time);
    formData.append('end_time', end_time);
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
                alert("Start Time > End Time!");
                return
            }

            if (!annotator_valid_flag){
                alert("Annotator not valid!");
                return
            }

            clean_screen_record();

            if (essay_record_length > ocr_record_length){
                for(i=0;i<ocr_record_length;i++){
                    add_tr_to_table(response['screen_essay_record'][i],response['screen_ocr_record'][i])
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
                        add_tr_to_table(response['screen_essay_record'][i],response['screen_ocr_record'][i])
                    }
                    for(i=essay_record_length;i<ocr_record_length;i++){
                        var tr = document.createElement("tr");
                        var td_essay_record = document.createElement("td");
                        var td_ocr_record = document.createElement("td");
                        var td_ocr_image = document.createElement("td");
                        var a_ocr_image = document.createElement("a");
                        var img_ocr_image = document.createElement("img");
                        td_essay_record.innerHTML = "";
                        td_ocr_record.innerHTML = JSON.stringify(response['screen_ocr_record'][i],null, 4);

                        a_ocr_image.setAttribute("href",response['screen_ocr_record'][i]['image_url']);
                        a_ocr_image.setAttribute("target","view_window");
                    
                        img_ocr_image.setAttribute("src",response['screen_ocr_record'][i]['image_url']);
                        img_ocr_image.setAttribute("width","70%");

                        a_ocr_image.appendChild(img_ocr_image);
                        td_ocr_image.appendChild(a_ocr_image);
                        tr.appendChild(td_essay_record);
                        tr.appendChild(td_ocr_record);
                        tr.appendChild(td_ocr_image);
                        record_area.appendChild(tr);
                    }
                }
                else{
                    for(i=0;i<essay_record_length;i++){
                        add_tr_to_table(response['screen_essay_record'][i],response['screen_ocr_record'][i])
                    }
                }
            }            
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Please check the time format!\n\n' + textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
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
function add_tr_to_table(screen_essay_record, screen_ocr_record){
    var tr = document.createElement("tr");
    var td_essay_record = document.createElement("td");
    var td_ocr_record = document.createElement("td");
    var td_ocr_image = document.createElement("td");
    var a_ocr_image = document.createElement("a");
    var img_ocr_image = document.createElement("img");

    td_essay_record.innerHTML = JSON.stringify(screen_essay_record,null, 4);
    td_ocr_record.innerHTML = JSON.stringify(screen_ocr_record,null, 4);

    a_ocr_image.setAttribute("href",screen_ocr_record['image_url']);
    a_ocr_image.setAttribute("target","view_window");
                    
    img_ocr_image.setAttribute("src",screen_ocr_record['image_url']);
    img_ocr_image.setAttribute("width","70%");

    a_ocr_image.appendChild(img_ocr_image);
    td_ocr_image.appendChild(a_ocr_image);
    tr.appendChild(td_essay_record);
    tr.appendChild(td_ocr_record);
    tr.appendChild(td_ocr_image);
    record_area.appendChild(tr);
}