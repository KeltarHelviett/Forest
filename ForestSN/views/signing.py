from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login as login_view
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from ..forms import OAuth2Form
from .utils import RedirectAuthenticatedUser
from ..models import AuthorizationCode, AccessToken

from secrets import token_urlsafe

@RedirectAuthenticatedUser
def log_in(request):
    """Log in page"""

    return login_view(request)

def sign_up(request):
    """Sign up page"""
    if 'auth_code' in request.GET:
        auth_code = request.GET['auth_code']
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

class OAuth2(View):
    methods = {
        '/api/login': 'login',
        '/api/token': 'token'
    }

    def _get_login(self, request):
        try:
            context = {'form': OAuth2Form()}
            context['redirect_url'] = request.GET['redirect_url']
        except MultiValueDictKeyError as error:
            return HttpResponseBadRequest(
                content="Required parameter {} wasn't specified".format(error.args[0])
            )

        return render(request, 'ForestSN/oauth.html', context=context)

    def _post_login(self, request):
        form = OAuth2Form(request.POST)
        user = request.user
        context = {
            'redirect_url': request.POST['redirect_url'],
            'form': form
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                context['form'] = OAuth2Form()
                return render(request, 'ForestSN/oauth.html', context=context)
            login(request, user)
        
        if user.is_authenticated:
            auth_code = AuthorizationCode(user=user)
            auth_code.save()
            url = request.POST['redirect_url'] + '?auth_code={}'.format(auth_code.code)
            return redirect(url)

        context['form'] = OAuth2Form()
        

        return render(request, 'ForestSN/oauth.html', context=context)

    def _post_token(self, request):
        auth_code = request.POST['auth_code']
        try:
           auth_code = AuthorizationCode.objects.get(code=auth_code)
           access_token = AccessToken(auth_code.user)
           access_token.save()
           return JsonResponse({
               'status': 'ok',
               'user_id': auth_code.user.id,
               'token': access_token.token
           })
        except:
            return JsonResponse({'status': 'error'}) 

    def get(self, request):
        return getattr(self, '_get_' + OAuth2.methods[request.path])(request)

    def post(self, request):
        return getattr(self, '_post_' + OAuth2.methods[request.path])(request)
