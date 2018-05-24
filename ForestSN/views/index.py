from django.shortcuts import render

from .utils import RedirectAuthenticatedUser

@RedirectAuthenticatedUser
def index(request):
    """Index page"""

    return render(request, 'ForestSN/index.html')
