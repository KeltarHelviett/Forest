from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view

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
    context = {'owner': owner}

    return render(request, 'ForestSN/profile.html', context=context)

def me(request): #pylint: disable=C0103
    """Authenticated user's profile.
    Shortcut for /profile/request.user.id"""

    return profile(request, request.user.id)
