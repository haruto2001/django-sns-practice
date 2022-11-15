import uuid

from django_cleanup import cleanup
from stdimage.models import StdImageField

from django.db import models
from django.contrib.auth.models import User


def image_directory_path(instance, filename):
    """ユニークなIDを生成して元のファイル名の拡張子を結合"""
    return f'images/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = StdImageField(upload_to=image_directory_path, blank=True, null=True, variations={
        # アスペクト比を保ったままリサイズ
        # サムネイル用の画像が別途で保存されるため同時に2枚の画像がデータベースに送られる
        'thumbnail': {'width': 500, 'height': 500}
        })
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='related_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # 投稿順にクエリを取得


class Comment(models.Model):
    """投稿に紐付いたコメント"""
<<<<<<< Updated upstream
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
=======
    name = models.CharField('Name', max_length=255)
    text = models.TextField('Comment')
>>>>>>> Stashed changes
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ["-created_at"]  # 投稿順にクエリを取得



class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username