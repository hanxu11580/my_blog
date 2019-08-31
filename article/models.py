from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from userprofile.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
import markdown

# Create your models here.

class Category(models.Model):
    cname = models.CharField(max_length=100)

class Tag(models.Model):
    tname = models.CharField(max_length=100)


class Test(models.Model):
    ccc = models.CharField(max_length=32)

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    body = RichTextField()

    created = models.DateTimeField(default=timezone.now)
#   default=timezone.now 表示创建数据时候自动将当前时间写入
    updated = models.DateTimeField(auto_now=True)
#   更新时自动写入当前时间
    views = models.PositiveIntegerField(default=0)
# PositiveInteger储存正整数字段
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    avatar = models.ImageField(upload_to='article/%Y%m%d/',null=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def increase_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

    def save(self, *args, **kwargs):
        article = super(ArticlePost,self).save(*args, **kwargs)

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            # (x, y) = image.size
            new_x = 150
            new_y = 150
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    def was_created_recently(self):
        diff = timezone.now() - self.created
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >=0 and diff.seconds < 60:
            return True
        else:
            return False



