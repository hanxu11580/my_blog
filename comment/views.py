from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Comment
from .forms import CommentForm
from article.models import ArticlePost
from userprofile.models import User

# Create your views here.

def post_comment(request, article_id):
    if request.session.get('is_login',None):
        article = get_object_or_404(ArticlePost,id=article_id)

        if request.method == 'POST':
            u_id = request.session.get('user_id')
            user = User.objects.get(id=u_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.user = user
                new_comment.save()


                return redirect(article)
            else:
                return HttpResponse('表单有误请重新填写.')
        else:
            return HttpResponse('暂不支持利用GET方式评论')

def hf_comment(request):
    if request.session.get('is_login', None):
        parent = request.GET.get('par')
        article_id = request.GET.get('article_id')
        article=get_object_or_404(ArticlePost,id=article_id)
        if request.method == 'POST':
            u_id = request.session.get('user_id')
            user = User.objects.get(id=u_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment=comment_form.save(commit=False)
                new_comment.article = article
                new_comment.parent_comment_id = parent
                new_comment.user = user

                # notify.send(
                #     user,
                #     recipient = parent.user,
                #     verb = '回复您',
                #     target = article,
                #     action_object = new_comment,
                # )
                new_comment.save()
                return redirect(article)
            else:
                return HttpResponse('输入有误')
        else:
            comment_form=CommentForm()
            context = {
                'parent':parent,
                'article_id':article_id,
                'comment_form':comment_form
            }
            return render(request, 'comment/hf.html',context)
    else:
        return HttpResponse('请先登录!')





