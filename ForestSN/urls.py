from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.sign_up, name='sign_up'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile_page'),
    path('me/', views.me, name='me'),
    path('media/upload_profile_img', views.upload_profile_img, name='upload_profile_img'),
    re_path(
        r'^media/imgs/user_(?P<user_id>[0-9]+)/img_(?P<img_id>[0-9]+)\.(jpg|jpeg|png|gif)/$',
        views.get_user_image
    ),
    path('post_api/', views.PostAPI.as_view())
]
