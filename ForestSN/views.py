from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def index(request):
    """Index page"""

    return render(request, 'ForestSN/index.html')

def sign_up(request):
    """Sign up page"""

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

def  profile(request, user_id):
    """Profile page"""
    owner = get_object_or_404(User, pk=user_id)
    context = {'owner': owner}

    return render(request, 'ForestSN/profile.html', context=context)
