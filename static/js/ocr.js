function previous(button) {
    console.log("Jump tp previous image...");

    var essay_id = Number(document.getElementById("essay_id").innerHTML);

    if (essay_id <= 0) {
        alert("There is no previous essay!");
        return
    }

    var formData = new FormData();
    formData.append('essay_id', essay_id);
    $.ajax({
        type: 'POST',
        url: '/mark_previous',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
            var previous_essay_id = document.getElementById("essay_id");
            previous_essay_id.innerHTML = essay_id - 1;
            var essay = document.getElementById("essay");
            essay.innerHTML = response;

            clearAllRadios();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function next(button) {
    console.log("Jump tp next essay...");

    var essay_id = Number(document.getElementById("essay_id").innerHTML);
    var essay_sum = Number(document.getElementById("sum").innerHTML) - 1;

    if (essay_id >= essay_sum ) {
        alert("There is no next essay!");
        return
    }

    var formData = new FormData();
    formData.append('essay_id', essay_id);
    $.ajax({
        type: 'POST',
        url: '/mark_next',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
            var next_essay_id = document.getElementById("essay_id");
            next_essay_id.innerHTML = essay_id + 1;
            var essay = document.getElementById("essay");
            essay.innerHTML = response;

            clearAllRadios();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}