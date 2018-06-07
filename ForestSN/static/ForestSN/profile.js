function reply(postId, wallOwnerId, text) {
    data = new FormData();
    data.append('post_id', postId);
    data.append('wall_owner_id', wallOwnerId);
    data.append('text', text.value);
    $.ajax({
        url: "/post_api/reply/",
        type: "POST",
        cache: false,
        processData: false,
        dataType: "json",
        data: data,
        contentType: false,
        "cstfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val()
    }).done((data) => {
        window.location.reload(false);
    })
}

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
    $('.post').click((e) => {
        console.log(e.target.tagName);
        if (e.target.tagName == 'A'|| e.target.tagName == 'SPAN')
            return;
        let self = e.currentTarget;
        window.location = location.protocol + '//' + location.host  +
                          location.pathname + '?post_id=' + $(self).data('post-id');
        return false;
    });
    $('.post-delete-btn').click((e) => {
        console.log('asd');
        let self = e.target;
        let res = confirm('You want to delete this post, don\'t you?');
        if (!res) return;
        $.ajax({
            url: "/post_api/?post_id=" + $(self).data('post-id'),
            type: "DELETE",
            cache: false,
            processData: false,
            dataType: "json",
            contentType: false,
            "cstfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val()
        }).done((data) => {
            window.location.reload(true); 
        })
    });
    $('a.post-reply').click((e) => {
        let self = e.currentTarget;
        let mediaWrapper = $(self).closest('.media');
        let postId = $(mediaWrapper).data('post-id');
        let replyBox = $(mediaWrapper).find('.reply-box')[0];
        let wallOwnerId = $('#wallOwnerId').val();
        $(replyBox).show();
        $(replyBox).html(`
            <div class='col'>
                <textarea style="width: 100%;" class="reply-text" cols="30" rows="2"></textarea>
                <button class="btn btn-primary float-right" onclick="reply(${postId}, ${wallOwnerId}, $(this).siblings('.reply-text')[0]);">Reply</button>
            </div>
        `)
    });
})
