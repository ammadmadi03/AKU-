$(document).ready(function() {
    console.log('upload_res.js script loaded');

    let maxEducationFields = 5; // Limit to 5 education fields
    let educationFieldCount = 1; // Start with one field

    function addEducationField() {
        if (educationFieldCount < maxEducationFields) {
            educationFieldCount++;
            if (educationFieldCount === 1) {
                $('#educationFields').append(`
                    <div class="form-group row">
                        <div class = "col-md-8">
                            <label for="education1">Education:</label>
                            <input type="text" class="form-control education-field" id="education${educationFieldCount}" name="qualification${educationFieldCount}" placeholder="Education">
                        </div>
                        <div class="col-md-4">
                            <label for="duration1">Duration:</label>
                            <input type="text" class="form-control duration-field" id="duration${educationFieldCount}" name="duration${educationFieldCount}" placeholder="Duration">
                        </div>
                    </div>
                `);
            }
            else {
                $('#educationFields').append(`
                    <div class="form-group row">
                        <div class = "col-md-8">
                            <input type="text" class="form-control education-field" id="education${educationFieldCount}" name="qualification${educationFieldCount}" placeholder="Education">
                        </div>
                        <div class="col-md-4">
                            <input type="text" class="form-control duration-field" id="duration${educationFieldCount}" name="duration${educationFieldCount}" placeholder="Duration">
                        </div>
                    </div>
                `);
            }
        }
    }

    // Event delegation to handle typing in dynamically added fields
    $('#educationFields').on('input', '.education-field', function() {
        let lastEducationField = $(`#education${educationFieldCount}`);
        if ($(this).is(lastEducationField) && $(this).val().length > 0) {
            addEducationField();
        }
    });

    $('#resume').on('change', function() {
        let formData = new FormData();
        formData.append('file', $('#resume')[0].files[0]);
        console.log('file selected');

        $.ajax({
            url: 'http://127.0.0.1:5000/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,

            success: function(response) {
                console.log(response);
                if (response.error) {
                    alert(response.error);
                } else {
                    $('#name').val(response.name || '');
                    $('#email').val(response.email || '');
                    $('#phone').val(response.phone || '');
                    $('#skills').val(response.skills || '');

                    if (response.education && Array.isArray(response.education)) {
                        // Clear existing fields
                        $('#educationFields').empty();
                        educationFieldCount = 0;

                        // Populate education fields
                        response.education.forEach((edu, index) => {
                            if (educationFieldCount < maxEducationFields) {
                                addEducationField();
                                $(`#education${educationFieldCount}`).val(edu);
                            }
                        });

                        // Add one more empty field if less than max
                        if (educationFieldCount < maxEducationFields) {
                            addEducationField();
                        }
                    } 

                    console.log('Showing verification message');
                    $('#verificationMessage').show();
                }
            },

            error: function(xhr, status, error) {
                console.error('Error:', {
                    readyState: xhr.readyState,
                    status: xhr.status,
                    statusText: xhr.statusText,
                    responseText: xhr.responseText
                });
            }
        });
    });
});
