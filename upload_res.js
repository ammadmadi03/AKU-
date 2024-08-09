$(document).ready(function() {
    console.log('upload_res.js script loaded');

    $('#resume').on('change', function() {
        // event.preventDefault();
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