function previous(button) {
    console.log("Jump tp previous essay...");

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
    var essay_sum = 9

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
    console.log("Submit annotation data...");

    if (isRadioChecked("overall_score")) {
        var overall_score = Number(document.querySelector('input[name="overall_score"]:checked').value);
    }
    else {
        alert("Please choose the Overall Score!");
        return
    }

    if (isRadioChecked("vocabulary_score")) {
        var vocabulary_score = Number(document.querySelector('input[name="vocabulary_score"]:checked').value);
    }
    else {
        alert("Please choose the Vocabulary Score!");
        return
    }

    if (isRadioChecked("sentence_score")) {
        var sentence_score = Number(document.querySelector('input[name="sentence_score"]:checked').value);
    }
    else {
        alert("Please choose the Sentence Score!");
        return
    }
    
    if (isRadioChecked("structure_score")) {
        var structure_score = Number(document.querySelector('input[name="structure_score"]:checked').value);
    }
    else {
        alert("Please choose the Structure Score!");
        return
    }
    
    if (isRadioChecked("content_score")) {
        var content_score = Number(document.querySelector('input[name="content_score"]:checked').value);
    }
    else {
        alert("Please choose the Content Score!");
        return
    }

    var essay_id = Number(document.getElementById("essay_id").innerHTML);


    var formData = new FormData();
    formData.append('essay_id', essay_id);
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
            var new_essay_id = document.getElementById("essay_id");
            new_essay_id.innerHTML = essay_id + 1;
            var annotated_quantity = document.getElementById("annotated_quantity");
            annotated_quantity.innerHTML = response['annotated_quantity'];
            var ratio = document.getElementById("ratio");
            ratio.innerHTML = response['annotation_ratio'];
            var essay = document.getElementById("essay");
            essay.innerHTML = response['essay'];

            clearAllRadios();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function setRadioUnchecked(name) {
    var radio = document.getElementsByName(name);
    for (var i = 0; i < radio.length; i++) {
        radio[i].checked = false;
    }
}

function clearAllRadios() {
    setRadioUnchecked("overall_score");
    setRadioUnchecked("vocabulary_score");
    setRadioUnchecked("sentence_score");
    setRadioUnchecked("structure_score");
    setRadioUnchecked("content_score");
}