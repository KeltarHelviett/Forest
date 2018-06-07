from django.views import View
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core import serializers

import json

from ..models import Post

class PostAPI(View):

    def get(self, request):
        pass

    def post(self, request):
        next_url = request.POST.get('next', '/')

        if request.path == '/post_api/reply/':
            try:
                parent_post = get_object_or_404(Post, pk=int(request.POST['post_id']))
                root_post = parent_post.root_post
                if root_post is None:
                    root_post = parent_post
                post = Post(
                    wall_owner=get_object_or_404(User, pk=int(request.POST['wall_owner_id'])),
                    author=get_object_or_404(User, pk=request.user.id),
                    text=request.POST['text'],
                    root_post=root_post,
                    parent_post=parent_post
                )
                post.save()
                return HttpResponse(serializers.serialize('json', [post]))
            except:
                return HttpResponseBadRequest('bad')

        try:
            post = Post(
                wall_owner=get_object_or_404(User, pk=int(request.POST['wall_owner_id'])),
                author=get_object_or_404(User, pk=int(request.POST['author_id'])),
                text=request.POST['text'],
                root_post=None,
                parent_post=None
            )
            post.save()
            return HttpResponseRedirect(next_url)
        except:
            return HttpResponseBadRequest('bad')

    def delete(self, request):
        try:
            post = get_object_or_404(Post, pk=int(request.GET['post_id']))
            post.delete()
            return HttpResponse(json.dumps({'success': True}))
        except:
            return HttpResponseBadRequest('bad')
