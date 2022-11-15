from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Post, Comment, Connection


class Home(LoginRequiredMixin, ListView):
    """HOMEで自分以外のユーザの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        # リクエストユーザのみ除外
        return Post.objects.exclude(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #get_or_createにしないとサインアップ時オブジェクトがないためエラーになる
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.filter(target=self.kwargs['pk'])
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """投稿編集ページ"""
    model = Post
    template_name = 'update.html'
    fields = ['title', 'content', 'image']

    def get_success_url(self, **kwargs):
        """編集完了後の遷移先"""
        pk = self.kwargs['pk']
        return reverse_lazy('detail', kwargs={"pk": pk})

    def test_func(self, **kwargs):
        """アクセスできるユーザを制限"""
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """投稿削除ページ"""
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('mypost')

    def test_func(self, **kwargs):
        """アクセスできるユーザを制限"""
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class CreatePost(LoginRequiredMixin, CreateView):
    """投稿フォーム"""
    model = Post
    template_name = 'create.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('mypost')

    def form_valid(self, form):
        """投稿ユーザとリクエストユーザを紐付け"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class LikeBase(LoginRequiredMixin, View):
    """いいねのベース．リダイレクト先は継承先で設定"""
    def get(self, request, *args, **kwargs):
        # 記事の特定
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)

        # いいねテーブル内に既にユーザが存在する場合
        if self.request.user in related_post.like.all():
            # テーブルからユーザを削除
            obj = related_post.like.remove(self.request.user)
        # いいねテーブル内にユーザが存在しない場合
        else:
            obj = related_post.like.add(self.request.user)
        return obj


class LikeHome(LikeBase):
    """HOMEページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        # LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect('home')


class LikeDetail(LikeBase):
    """詳細ページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        # LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('detail', pk)


class CreateComment(LoginRequiredMixin, CreateView):
    """コメント投稿フォーム"""
    model = Comment
    template_name = 'comment.html'
    fields = ['name', 'text', 'target']

    # フォームの内容にコメントの対象を付加して保存
    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.name = self.request.user
        comment.target = post
        comment.save()
        return redirect('detail', pk=post_pk)


class FollowBase(LoginRequiredMixin, View):
    """フォローのベース．リダイレクト先は継承先で設定"""
    def get(self, request, *args, **kwargs):
        # ユーザの特定
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user

        # ユーザ情報からコネクション情報を取得．存在しなければ作成
        my_connection = Connection.objects.get_or_create(user=self.request.user)

        # フォローテーブル内に既にユーザが存在する場合
        if target_user in my_connection[0].following.all():
            # テーブルからユーザを削除
            obj = my_connection[0].following.remove(target_user)
        # フォローテーブル内にユーザが存在しない場合
        else:
        # テーブルにユーザを追加
            obj = my_connection[0].following.add(target_user)
            return obj


class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        # FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect('home')


class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        # FollwBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('detail', pk)


class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザの投稿をリスト表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        """フォローリスト内にユーザが含まれている場合のみクエリセットを返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()
        # 投稿ユーザがフォローしているユーザに含まれている場合オブジェクトを返す．
        return Post.objects.filter(user__in=all_follow)

    def get_context_data(self, *args, **kwargs):
        """コネクションに関するオブジェクト情報をコンテクストに追加"""
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context









