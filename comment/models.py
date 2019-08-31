from django.db import models
from userprofile.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField
# from mptt.models import MPTTModel, TreeForeignKey

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', related_name='p_comment', null=True, blank=True,on_delete=models.CASCADE)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[0:20]

class Comment_News(models.Model):
    send_user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(default='回复您')
    description = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)




