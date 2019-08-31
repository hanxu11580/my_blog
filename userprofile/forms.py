
from django.forms import forms,fields,widgets
# from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.forms import ModelForm
from userprofile.models import User


# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()


class UserForm(forms.Form):
    name = fields.CharField(label="用户名", max_length=128, widget=widgets.TextInput(attrs={'class':'form-control',
                                                                                             'placeholder':"Username",
                                                                                             'autofocus': ''}))


    password = fields.CharField(label="密码", max_length=256, widget=widgets.PasswordInput(attrs={'class': 'form-control',
                                                                                            'placeholder': "Password",
                                                                                            }))
    captcha = CaptchaField(label='验证码')

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = {'phone', 'avatar','bio'}






class RegisterForm(forms.Form):
    gender=(
        ('male', '男'),
        ('female', '女'),
    )

    name = fields.CharField(label='用户名：', max_length=128, widget=widgets.TextInput(attrs={'class': 'form-control'}))
    password1 = fields.CharField(label='密码', max_length=256, widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    password2 = fields.CharField(label='确认密码', max_length=256, widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = fields.EmailField(label='邮箱地址', widget=widgets.EmailInput(attrs={'class': 'form-control'}))
    sex = fields.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

class ModifyForm(forms.Form):
    name = fields.CharField(label='用户名',max_length=128,disabled=True)
    old_password = fields.CharField(label='旧密码', max_length=256)
    new_password = fields.CharField(label='新密码', max_length=256)

