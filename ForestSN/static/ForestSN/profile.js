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
    });
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $('#profile-img-form').submit(function (e) {
        e.preventDefault();
        let data = new FormData($("#profile-img-form")[0]);
        console.log($("#profile-img-form"));
        $.ajax({
            url: "/media/upload_profile_img",
            type: "POST",
            data: data,
            cache: false,
            processData: false,
            dataType: "json",
            contentType: false,
            success: function (data) {
                $("#profile-img").attr('src', data.url);
            },
            error: function(data) {
            },
            "cstfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val()
        });
        return false;
    });
    $('#upload-profile-img-btn').click(function () {
        $('#profile-img-input').click();
    });
    $('#profile-img-input').change(function (d) {
        $('#profile-img-form').submit();
    });
})
