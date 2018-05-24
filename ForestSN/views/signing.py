from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login as login_view

from .utils import RedirectAuthenticatedUser

@RedirectAuthenticatedUser
def log_in(request):
    """Log in page"""

    return login_view(request)

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
