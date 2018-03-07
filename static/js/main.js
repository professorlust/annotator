function previous(button) {
    console.log("Previous");

    var essay_id = document.getElementById("essay_id").innerHTML;
    console.log(essay_id)

    if (essay_id == 0) {
        alert("There is no previous essay!");
        return
    }

    var formData = new FormData();
    formData.append('essay_id', essay_id);
    $.ajax({
        type: 'POST',
        url: '/previous',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function next(button) {
    console.log("Next");

    var essay_id = document.getElementById("essay_id").innerHTML;
    var essay_sum = 9

    if (essay_id == essay_sum ) {
        alert("There is no next essay!");
        return
    }

    var formData = new FormData();
    formData.append('essay_id', essay_id);
    $.ajax({
        type: 'POST',
        url: '/next',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function isRadioChecked(name) {
    var radio = document.getElementsByName(name);
    var is_checked = false;
    for (var i = 0; i < radio.length; i++) {
        if (radio[i].checked) {
            is_checked = true;
            break;
        }
    }
    return is_checked;
}

function submit(button) {
    console.log("Submit");

    if (isRadioChecked("overall_score")) {
        var overall_score = document.querySelector('input[name="overall_score"]:checked').value;
    }
    else {
        alert("Please choose the Overall Score!");
        return
    }

    if (isRadioChecked("vocabulary_score")) {
        var vocabulary_score = document.querySelector('input[name="vocabulary_score"]:checked').value;
    }
    else {
        alert("Please choose the Vocabulary Score!");
        return
    }

    if (isRadioChecked("sentence_score")) {
        var sentence_score = document.querySelector('input[name="sentence_score"]:checked').value;
    }
    else {
        alert("Please choose the Sentence Score!");
        return
    }
    
    if (isRadioChecked("structure_score")) {
        var structure_score = document.querySelector('input[name="structure_score"]:checked').value;
    }
    else {
        alert("Please choose the Structure Score!");
        return
    }
    
    if (isRadioChecked("content_score")) {
        var content_score = document.querySelector('input[name="content_score"]:checked').value;
    }
    else {
        alert("Please choose the Content Score!");
        return
    }

    var formData = new FormData();
    formData.append('overall_score', overall_score);
    formData.append('vocabulary_score', vocabulary_score);
    formData.append('sentence_score', sentence_score);
    formData.append('structure_score', structure_score);
    formData.append('content_score', content_score);
    $.ajax({
        type: 'POST',
        url: '/mark',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}