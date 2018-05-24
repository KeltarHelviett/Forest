from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from ..forms import UserProfileForm


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
