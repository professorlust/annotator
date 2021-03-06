function previousEssay(button) {
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
            essay.innerHTML = response['essay'];
            var essay_annotator_mark = document.getElementById("annotator_mark");
            essay_annotator_mark.innerHTML = response['essay_annotator_mark'];

            clearAllMarks();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function nextEssay(button) {
    console.log("Jump tp next essay...");

    var essay_id = Number(document.getElementById("essay_id").innerHTML);
    var essay_sum = Number(document.getElementById("sum").innerHTML);

    if (essay_id >= (essay_sum - 1)) {
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
            essay.innerHTML = response['essay'];
            var essay_annotator_mark = document.getElementById("annotator_mark");
            essay_annotator_mark.innerHTML = response['essay_annotator_mark'];

            clearAllMarks();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function jumpImage(button) {
    console.log("Jump tp an essay...");

    var jump_id = Number(document.getElementById("jump_id").value);
    var essay_sum = Number(document.getElementById("sum").innerHTML);

    if (jump_id >= essay_sum || jump_id < 0) {
        alert("There is no such image!");
        return
    }

    var formData = new FormData();
    formData.append('jump_id', jump_id);
    $.ajax({
        type: 'POST',
        url: '/mark_jump',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');

            var jump_essay_id = document.getElementById("essay_id");
            jump_essay_id.innerHTML = jump_id;
            var essay = document.getElementById("essay");
            essay.innerHTML = response['essay'];
            var essay_annotator_mark = document.getElementById("annotator_mark");
            essay_annotator_mark.innerHTML = response['essay_annotator_mark'];

            clearAllMarks();
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert(textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}

function submitEssayMark(button) {
    console.log("Submit essay annotation data...");

    var overall_score = document.getElementById("overall_score").value;

    if (overall_score == '') {
        alert("Please enter the Overall Socre!");
        return
    }

    if (overall_score < 0 || overall_score > 15) {
        alert("Overall Socre is between 0 and 15 (inclusive)!");
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
        url: '/mark_submit',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function(response) {
            console.log('Response received!');

            var empty_flag = response['empty_flag'];
            if (empty_flag) {
                alert("All the essays have been marked");
                var annotated_essay_quantity = document.getElementById("annotated_quantity");
                annotated_essay_quantity.innerHTML = response['annotated_essay_quantity'];
                var essay_annotator_mark = document.getElementById("annotator_mark");
                essay_annotator_mark.innerHTML = response['essay_annotator_mark']; 
                var ratio = document.getElementById("ratio");
                ratio.innerHTML = response['annotation_essay_ratio'];
                return
            }

            var invalid_flag = response['invalid_flag'];
            if (invalid_flag) {
                alert("Submission invalid! This essay has been marked by two persons");
                var annotated_essay_quantity = document.getElementById("annotated_quantity");
                annotated_essay_quantity.innerHTML = response['annotated_essay_quantity'];
                var essay_annotator_mark = document.getElementById("annotator_mark");
                essay_annotator_mark.innerHTML = response['essay_annotator_mark']; 
                var ratio = document.getElementById("ratio");
                ratio.innerHTML = response['annotation_essay_ratio'];
                return
            }

            var new_essay_id = document.getElementById("essay_id");
            new_essay_id.innerHTML = response["essay_id"];
            var annotated_essay_quantity = document.getElementById("annotated_quantity");
            annotated_essay_quantity.innerHTML = response['annotated_essay_quantity'];
            var ratio = document.getElementById("ratio");
            ratio.innerHTML = response['annotation_essay_ratio'];
            var essay = document.getElementById("essay");
            essay.innerHTML = response['essay'];
            var essay_annotator_mark = document.getElementById("annotator_mark");
            essay_annotator_mark.innerHTML = response['essay_annotator_mark'];            

            clearAllMarks();
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

function clearMark(button) {
    clearAllMarks();
}

function setRadioUnchecked(name) {
    var radio = document.getElementsByName(name);
    for (var i = 0; i < radio.length; i++) {
        radio[i].checked = false;
    }
}

function clearAllMarks() {
    document.getElementById("overall_score").value = '';
    setRadioUnchecked("vocabulary_score");
    setRadioUnchecked("sentence_score");
    setRadioUnchecked("structure_score");
    setRadioUnchecked("content_score");
}