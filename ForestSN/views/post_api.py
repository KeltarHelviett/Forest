from django.views import View
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from ..models import Post

class PostAPI(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            post = Post(
                wall_owner=get_object_or_404(User, pk=int(request.POST['wall_owner_id'])),
                author=get_object_or_404(User, pk=int(request.POST['author_id'])),
                text=request.POST['text'],
                root_post=None,
                parent_post=None
            )
            post.save()
            next_url = request.POST.get('next', '/')
            return HttpResponseRedirect(next_url)
        except:
            return HttpResponseBadRequest('bad')
    
    def delete(self, request):
        pass        
