$(document).ready(function () {
    $('#profile-img-upload-progress').hide();
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
        $('#profile-img-upload-progress').show();
        $('#upload-profile-img-btn').hide();
        let data = new FormData($("#profile-img-form")[0]);
        console.log($("#profile-img-form"));
        $.ajax({
            xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.addEventListener("progress", function(evt){
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    $('#profile-img-upload-progress-bar').css('width', Math.ceil(percentComplete) * 100 + '%');
                }
            }, false);

            return xhr;
            },
            url: "/media/upload_profile_img",
            type: "POST",
            data: data,
            cache: false,
            processData: false,
            dataType: "json",
            contentType: false,
            "cstfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val()
        }).always((data) => {
            window.setTimeout(() => {
                $('#profile-img-upload-progress').hide();
                $('#upload-profile-img-btn').show();
            }, 600);
        }).done((data) => {
            window.setTimeout(() => {
                $("#profile-img").attr('src', data.url);
                $('#profileImageModal').modal('hide');
            }, 500);
        }).fail((data) => {
            $('#profileImageModal').modal('hide');
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
