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
            console.log('Response received!');
            alert('Essay Grading Annotation:\n' + JSON.stringify(response['essay_progress']) + '\n\nOCR Result Annotation:\n' + JSON.stringify(response['essay_progress']));
    
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('Please check the date format!\n\n' + textStatus + ' - ' + errorThrown + '\n\n' + jqXHR.responseText);
            console.log("Something went wrong:(");
        }
    });
}