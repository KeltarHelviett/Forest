from django.http.response import HttpResponse, HttpResponseBadRequest
from wsgiref.util import FileWrapper
import json, mimetypes, os

from ..models import UserImage

def upload_profile_img(request):
    if request.method == "POST":
        img = request.FILES['profile-img']
        if 'image' not in img.content_type:
            return HttpResponseBadRequest('It\' probably not an image')
        user_img = UserImage(img=img, user=request.user)
        user_img.save()
        user_profile = request.user.userprofile
        user_profile.profile_img = user_img
        user_profile.save()
        return HttpResponse(json.dumps({'url': user_img.img.url}))
    return HttpResponseBadRequest()

def get_user_image(request, user_id, img_id):
    if request.method == "GET":
        try:
            user_img = UserImage.objects.get(pk=int(img_id))
        except: #pylint: disable=W0702
            return HttpResponseBadRequest()
        img = user_img.img
        wrapper = FileWrapper(open(img.path, 'rb'))
        content_type = mimetypes.guess_type(os.path.basename(img.path))
        response = HttpResponse(wrapper, content_type=content_type)
        return response
