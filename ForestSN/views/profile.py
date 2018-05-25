from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View

from ..forms import UserProfileForm
from ..models import Post

class ProfileView(View):
    """Profile view"""

    def dispatch(self, request, user_id):
        self.owner = get_object_or_404(User, pk=user_id)

        self.posts = Post.objects.filter(
            wall_owner=self.owner,
            parent_post=None,
            root_post=None
        ).order_by('-pub_date')

        self.form = UserProfileForm(
            initial={
                'email': self.owner.email,
                'first_name': self.owner.userprofile.first_name,
                'last_name': self.owner.userprofile.last_name
            }
        )

        self.context = {'owner': self.owner, 'form': self.form, 'posts': self.posts}

        return super().dispatch(request, user_id)

    def get(self, request, user_id):
        if 'post_id' in request.GET:
            pk = int(request.GET['post_id']) #pylint: disable=C0103
            self.context['viewed_post'] = get_object_or_404(Post, pk=pk)
            self.context['viewed_post_comments'] = Post.objects.filter(
                root_post__pk=pk
            ).order_by(
                '-pub_date'
            )

        return render(request, 'ForestSN/profile.html', context=self.context)

    def post(self, request, user_id):
        self.form = UserProfileForm(request.POST)

        if self.form.is_valid():
            self.owner.userprofile.first_name = self.form.cleaned_data['first_name']
            self.owner.userprofile.last_name = self.form.cleaned_data['last_name']
            self.owner.email = self.form.cleaned_data['email']
            self.owner.userprofile.save()
            self.owner.save()
            return redirect('/profile/{}'.format(self.owner.id))

        return render(request, 'ForestSN/profile.html', context=self.context)

def me(request): #pylint: disable=C0103
    """Authenticated user's profile.
    Shortcut for /profile/request.user.id"""

    return ProfileView.as_view()(request, request.user.id)
