$(document).ready(function () {
    let btn = $('#edit-btn');
    if (btn) {
        btn.click(function () {
            $(this).css('display', 'none');
            $('#cancel-btn').css('display', 'inline');
            $('#save-profile-btn').css('display', 'inline');
            $('#profile-fieldset').prop('disabled', false);
        })
    }
    $('#cancel-btn').click(function () {
        $(this).css('display', 'none');
        $('#save-profile-btn').css('display', 'none');
        $('#edit-btn').css('display', 'inline');
        $('#profile-fieldset').prop('disabled', true);        
    })
})