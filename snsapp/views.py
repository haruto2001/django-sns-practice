from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Post


class Home(LoginRequiredMixin, ListView):
    """HOMEで自分以外のユーザの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        # リクエストユーザのみ除外
        return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        # 自分の投稿に限定
        return Post.objects.filter(user=self.request.user)

class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'detail.html'