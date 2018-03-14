function previous(button) {
    console.log("Jump tp previous image...");

    var ocr_id = Number(document.getElementById("ocr_id").innerHTML);

    if (ocr_id <= 0) {
        alert("There is no previous image!");
        return
    }

    var formData = new FormData();
    formData.append('ocr_id', ocr_id);
    $.ajax({
        type: 'POST',
        url: '/ocr_previous',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');

            var previous_ocr_id = document.getElementById("ocr_id");
            previous_ocr_id.innerHTML = ocr_id - 1;

            var previous_image_url = document.getElementById("image_url");
            previous_image_url.src = response["image_url"];

            var previous_ocr_essay = document.getElementById("ocr_essay");
            previous_ocr_essay.value = response["ocr_essay"];

            var previous_ocr_correction = document.getElementById("ocr_correction");
            previous_ocr_correction.value = response["ocr_essay"];
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function next(button) {
    console.log("Jump tp next image...");

    var ocr_id = Number(document.getElementById("ocr_id").innerHTML);
    var ocr_sum = Number(document.getElementById("sum").innerHTML) - 1;

    if (ocr_id >= ocr_sum ) {
        alert("There is no next image!");
        return
    }

    var formData = new FormData();
    formData.append('ocr_id', ocr_id);
    $.ajax({
        type: 'POST',
        url: '/ocr_next',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');

            var next_ocr_id = document.getElementById("ocr_id");
            next_ocr_id.innerHTML = ocr_id + 1;

            var next_image_url = document.getElementById("image_url");
            next_image_url.src = response["image_url"];

            var next_ocr_essay = document.getElementById("ocr_essay");
            next_ocr_essay.value = response["ocr_essay"];

            var next_ocr_correction = document.getElementById("ocr_correction");
            next_ocr_correction.value = response["ocr_essay"];
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}


function submit(button) {
    console.log("Submit OCR result correction data...");

    var ocr_id = Number(document.getElementById("ocr_id").innerHTML);
    var image_url = document.getElementById("image_url").src;
    var ocr_correction = document.getElementById("ocr_correction").innerHTML;

    var formData = new FormData();
    formData.append('ocr_id', ocr_id);
    formData.append('image_url', image_url);
    formData.append('ocr_correction', ocr_correction);
    $.ajax({
        type: 'POST',
        url: '/ocr_submit',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
            var new_ocr_id = document.getElementById("ocr_id");
            new_ocr_id.innerHTML = response["ocr_id"];
            
            var new_image_url = document.getElementById("image_url");
            new_image_url.src = response["image_url"];

            var corrected_ocr_quantity = document.getElementById("annotated_quantity");
            corrected_ocr_quantity.innerHTML = response['corrected_ocr_quantity'];
            
            var ratio = document.getElementById("ratio");
            ratio.innerHTML = response['corrected_ocr_ratio'];
            
            var new_ocr_essay = document.getElementById("ocr_essay");
            new_ocr_essay.innerHTML = response["ocr_essay"];

            var new_ocr_correction = document.getElementById("ocr_correction");
            new_ocr_correction.innerHTML = response["ocr_essay"];
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}


