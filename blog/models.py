from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('カテゴリ', max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# CategoryモデルとPostモデルの連携
	# on_delete=models.PROTECTはカテゴリを削除したときに同時に投稿が削除されるのを防げる(on_delete=models.CASCADEはカテゴリ消したら同時に投稿も消える)
	category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
	title = models.CharField("タイトル", max_length=200)
	image = models.ImageField(upload_to='images', verbose_name='イメージ画像', null=True, blank=True)
	content = models.TextField("本文")
	created = models.DateTimeField("作成日", default=timezone.now)

	def __str__(self):
		return self.title
