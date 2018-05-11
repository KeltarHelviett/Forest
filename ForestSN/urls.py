from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.sign_up, name='sign_up')
]
