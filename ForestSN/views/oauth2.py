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

from requests import post
from secrets import token_urlsafe

class OAuth2(View):
    methods = {
        '/api/login': 'login',
        '/api/token': 'token'
    }

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OAuth2, self).dispatch(request, *args, **kwargs)

    def _get_login(self, request, *args, **kwargs):
        try:
            context = {'form': OAuth2Form()}
            context['redirect_url'] = request.GET['redirect_url']
            context['service_id'] = request.GET['service_id']
        except MultiValueDictKeyError as error:
            return HttpResponseBadRequest(
                content="Required parameter {} wasn't specified".format(error.args[0])
            )

        return render(request, 'ForestSN/oauth.html', context=context)

    def _post_login(self, request, *args, **kwargs):
        form = OAuth2Form(request.POST)
        user = request.user
        context = {
            'redirect_url': request.POST['redirect_url'],
            'service_id': request.POST['service_id'],
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
            auth_code = AuthorizationCode(user=user, service=context['service_id'])
            auth_code.save()
            url = request.POST['redirect_url'] + '?auth_code={}'.format(auth_code.code)
            return redirect(url)

        context['form'] = OAuth2Form()

        return render(request, 'ForestSN/oauth.html', context=context)

    def _post_token(self, request, *args, **kwargs):
        try:
            auth_code = request.POST['auth_code']
            service_id = request.POST['serivce_id']
            auth_code = AuthorizationCode.objects.get(
                code=auth_code, service=service_id
            )
            access_token = AccessToken(user=auth_code.user, service=service_id)
            access_token.save()
            return JsonResponse({
                'status': 'ok',
                'user_id': auth_code.user.id,
                'token': access_token.token
            })
        except:
            return JsonResponse({'status': 'error'})

    def _get_profile(self, request, user_id=None):
        try:
            user = User.objects.get(pk=user_id)
            data = {
                'status': 'ok',
                'email': user.userprofile.email,
                'login': user.username
            }
            return JsonResponse(data)
        except:
            return JsonResponse({'status': 'error'})

    def get(self, request, user_id=None):
        if user_id is None:
            return getattr(self, '_get_' + OAuth2.methods[request.path])(request)
        return self._get_profile(request, user_id=user_id)

    def post(self, request, user_id=None):
        return getattr(self, '_post_' + OAuth2.methods[request.path])(request)
