from django.shortcuts import redirect

class RedirectAuthenticatedUser(object):

    def __init__(self, view):
        self.view = view

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/profile/{}'.format(request.user.id))
        return self.view(request, *args, **kwargs)
