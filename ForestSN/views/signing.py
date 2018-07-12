from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..forms import OAuth2Form
from .utils import RedirectAuthenticatedUser
from ..models import AuthorizationCode, AccessToken, ExternalSocialNetwork, ExternalSocialNetworkSession

from requests import post, get
from secrets import token_urlsafe

@RedirectAuthenticatedUser
def log_in(request):
    """Log in page"""

    return login_view(request)

def sign_up(request):
    """Sign up page"""
    sns = ExternalSocialNetwork.objects.all()
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

    context = {'form': form, 'sns': sns}
    return render(request, 'ForestSN/signup.html', context=context)

def external_sn_signup(request, sn_name=''):
    import traceback
    try:
        auth_code = request.GET['auth_code']
        esn = ExternalSocialNetwork.objects.get(name=sn_name)
        data = post(esn.url + 'token', data={
            'service_id': 'Forest',
            'auth_code': auth_code
        }).json()
        if data['status'] == 'ok':
            user = User(username=token_urlsafe(32), password=token_urlsafe(32))
            user.save()
            esns = ExternalSocialNetworkSession(
                user=user, access_token=data['token'],
                ext_user_id=data['user_id'], ext_social_network=esn
            )
            esns.save()
            try:
                data = get(esn.url + 'profile/{}?service_id={}&token={}'.format(
                    esns.ext_user_id, 'Forest', esns.access_token
                )).json()
                if data['status'] == 'ok':
                    user.email = data['email']
                    user.save()
            except:
                traceback.print_exc()
            login(request, user)
            return redirect('/me')
    except:
        return HttpResponseBadRequest('bad')
