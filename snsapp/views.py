from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import LiveView

from .models import Post


class Home(LoginRequiredMixin, LiveView):
    """HOMEで自分以外のユーザの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        # リクエストユーザのみ除外
        return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, LiveView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        # 自分の投稿に限定
        return Post.objects.filter(user=self.request.user)