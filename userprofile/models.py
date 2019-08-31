from django.db import models

# Create your models here.
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    superuser = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"] #创建的对象反时间排向，也就是新创建的在前面
        verbose_name = "用户" #单数
        verbose_name_plural = "用户" #复数