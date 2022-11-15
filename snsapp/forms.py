from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """新規投稿・投稿編集フォーム"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class CommentCreateForm(forms.ModelForm):
    """コメントフォーム"""
    class Meta:
        model = Comment
        exclude = ['target', 'created_at']