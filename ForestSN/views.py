from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view
from django.http.response import HttpResponse, HttpResponseBadRequest
from wsgiref.util import FileWrapper
import json, mimetypes, os

from .forms import UserProfileForm
from .models import UserImage

class RedirectAuthenticatedUser(object):

    def __init__(self, view):
        self.view = view

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/profile/{}'.format(request.user.id))
        return self.view(request, *args, **kwargs)

@RedirectAuthenticatedUser
def log_in(request):
    """Log in page"""

    return login_view(request)

@RedirectAuthenticatedUser
def index(request):
    """Index page"""
    if request.user.is_authenticated:
        return redirect('/profile/{}'.format(request.user.id))

    return render(request, 'ForestSN/index.html')

@RedirectAuthenticatedUser
def sign_up(request):
    """Sign up page"""
    if request.user.is_authenticated:
        return redirect('/profile/{}'.format(request.user.id))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'ForestSN/signup.html', context=context)

def profile(request, user_id):
    """Profile page"""

    owner = get_object_or_404(User, pk=user_id)

    form = UserProfileForm(
        initial={
            'email': owner.email,
            'first_name': owner.userprofile.first_name,
            'last_name': owner.userprofile.last_name
        }
    )
    context = {'owner': owner, 'form': form}

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            owner.userprofile.first_name = form.cleaned_data['first_name']
            owner.userprofile.last_name = form.cleaned_data['last_name']
            owner.email = form.cleaned_data['email']
            owner.userprofile.save()
            owner.save()
            return redirect('/profile/{}'.format(owner.id))

    return render(request, 'ForestSN/profile.html', context=context)

def me(request): #pylint: disable=C0103
    """Authenticated user's profile.
    Shortcut for /profile/request.user.id"""

    return profile(request, request.user.id)


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
        except:
            return HttpResponseBadRequest()
        img = user_img.img
        wrapper = FileWrapper(open(img.path, 'rb'))
        content_type = mimetypes.guess_type(os.path.basename(img.path))
        response = HttpResponse(wrapper, content_type=content_type)
        return response
