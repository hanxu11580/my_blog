from django.shortcuts import render,HttpResponse,redirect
# from userprofile.forms import UserLoginForm
from userprofile.forms import UserForm,RegisterForm,UserEditForm,ModifyForm
from django.contrib.auth import authenticate, login, logout
from userprofile import models
# Create your views here.

def user_login(request):
    # if request.method == 'POST':
    #     user_login_form = UserLoginForm(request.POST)
    #     if user_login_form.is_valid():
    #         data = user_login_form.cleaned_data
    #         user = authenticate(username=data['username'], password=data['password'])
    #         if user:
    #             login(request, user)
    #             return redirect('article:article_list')
    #         else:
    #             return HttpResponse('账号密码有误')
    #     else:
    #         return HttpResponse('账号密码输入不合法')
    # elif request.method == 'GET':
    #     user_login_form = UserLoginForm()
    #     context = {
    #         'form':user_login_form
    #     }
    #     return render(request, 'userprofile/login.html', context)
    # else:
    #     return HttpResponse('请使用GET或POST请求方式!')
    if request.session.get('is_login', None):
        return redirect('article:article_list')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请填写相关信息!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('name')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name = username)
            except:
                message = '用户名不存在！'
                return render(request, 'userprofile/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('article:article_list')

            else:
                message= '用户密码错误!'
                return render(request, 'userprofile/login.html',locals())
        else:
            return render(request, 'userprofile/login.html', locals())
    else:
        login_form = UserForm()
        return render(request, 'userprofile/login.html', locals())




# def user_logout(request):
#     logout(request)
#     return redirect('article:article_list')
def user_logout(request):
    if not request.session.get('is_login', None):
        return redirect('userprofile:login')
    request.session.flush()
    return redirect('article:article_list')


def user_register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = '请填写相关信息'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('name')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次密码不一致'
                return render(request, 'userprofile/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
            if same_name_user:
                message = '用户名已存在'
                return render(request, 'userprofile/register.html', locals())
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:
                message = '邮箱已经被注册'
                return render(request, 'userprofile/register.html', locals())

            new_user = models.User()
            new_user.name = username
            new_user.password = password1
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('userprofile:login')
        else:
            return render(request, 'userprofile/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'userprofile/register.html', locals())


def user_edit(request, id):
    if not request.session.get('is_login', None):
       return redirect('userprofile:login')

    user = models.User.objects.get(id=id)
    if request.method == 'POST':
        if request.session.get('user_id') != user.id:
            return HttpResponse('你无权修改此用户信息')

        user_form = UserEditForm(request.POST, request.FILES)
        if user_form.is_valid():
            user.phone = user_form.cleaned_data.get('phone')
            user.bio = user_form.cleaned_data.get('bio')
            if 'avatar' in request.FILES:
                user.avatar = user_form.cleaned_data.get('avatar')
            user.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('表单输入有误，请重新输入')
    elif request.method == 'GET':
            user_form = UserEditForm()
            return render(request, 'userprofile/edit.html', locals())
    else:
            return HttpResponse('请使用POST或GET方式访问')

def modify_password(request, id):
    user = models.User.objects.get(id=id)
    message = '请填写相关信息'
    if request.method == 'POST':
        modify_form = ModifyForm(request.POST,initial={'name': user.name})
        if modify_form.is_valid():
            password1 = modify_form.cleaned_data.get('old_password')
            password2 = modify_form.cleaned_data.get('new_password')
        if password1 != user.password:
            message='原来的密码输入有误！'
            return render(request, 'userprofile/modifypassword.html', locals())
        else:
            user.password = password2
            user.save()
            return redirect('userprofile:logout')
    else:
        modify_form = ModifyForm(initial={'name':user.name})
        return render(request, 'userprofile/modifypassword.html', locals())





