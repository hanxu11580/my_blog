from django.shortcuts import render,HttpResponse,redirect
from article.models import ArticlePost,Category,Tag
import markdown
from article.forms import ArticlePostForm
from userprofile.models import User
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm
from utils import page
from django_redis import get_redis_connection
# from django.core.cache import cache
# Create your views here.

def article_list(request):
    current_page = request.GET.get('page')
    all_count =ArticlePost.objects.all().count()
    page_info = page.PageInfo(current_page, all_count, 5,order=None,category=None,year=None,month=None,tag=None)
    article_list = ArticlePost.objects.all()

    article_list = article_list[page_info.start():page_info.end()]
    views_article_list = ArticlePost.objects.all().order_by('-views')[0:3]
    r = get_redis_connection()
    article_id_list = r.lrange(request.session.get('user_name'), 0, -1)
    redis_lists = []
    for i in article_id_list:
        redis_lists.append(ArticlePost.objects.get(id=i))

    context  ={
        'articles': article_list,
        'page_info':page_info,
        'views_article_list':views_article_list,
        'redis_lists':redis_lists,
    }

    return render(request, 'article/list.html', context)


def article_detail(request,id):
    '''
    记录用户访问的前5条记录，并储存在redis
    每个登陆的者的user_name为键，每个用户都有自己相应的redis list
    当没有登陆，redis lists的键为
    :param request:
    :param id:
    :return:
    '''
    user_name = request.session.get('user_name')
    r = get_redis_connection()
    if r.exists(user_name):
        lists = r.lrange(user_name, 0, -1)
        '''
        由于redis中list 中数字形式为b'10'类似这样的,所以需要转变为int型,才能和文章的id进行判断
        '''
        article_id_list = []
        for i in lists:
            article_id_list.append(int(i))
        if id not in article_id_list:
            if r.llen(user_name) < 5:
                r.lpush(user_name,id)
            else:
                r.rpop(user_name)
                r.lpush(user_name, id)
        else:
            pass
    else:
        r.lpush(user_name, id)
    r.expire(request.session.get('user_name'), 60*30) #超时为30分钟
    # print(r.ttl(request.session.get('user_name')))



    article = ArticlePost.objects.get(id=id)
    article.increase_view()
    article.body = markdown.markdown(article.body,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite'
    ])
    comments = Comment.objects.filter(article=id)#显示评论相关的东西如评论的发送的时间，用户名，总共有几条评论
    comment_form = CommentForm() #这个是为了显示ckeditor的评论的框

    context = {
        'article': article,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request, 'article/detail.html', context)


def article_create(request):
    if request.session.get('is_login', None):
        category_list = Category.objects.all()
        tag_list = Tag.objects.all()
        if request.method == 'POST':
            article_post_form = ArticlePostForm(request.POST,request.FILES)
            if article_post_form.is_valid():
                new_article = article_post_form.save(commit=False)
                uid = request.session.get('user_id')
                new_article.author = User.objects.get(id=uid)
                new_article.category = article_post_form.cleaned_data.get('category')
                new_article.save()
                # 这个save()是因为没有文章的id是无法建立多对多操作的
                for i in article_post_form.cleaned_data.get('tag'):
                    new_article.tag.add(i)
                new_article.save()
                return redirect('article:article_list')
            else:
                return HttpResponse('表单数据有误，请重新填写')
        else:
            article_post_form = ArticlePostForm()
            # context = {
            #     'article_post_form': article_post_form
            # }
            return render(request, 'article/create.html', locals())
    else:
        return HttpResponse('写文章前必须先登陆')


def article_delete(request, id):
    uname = request.session.get('user_name')
    article = ArticlePost.objects.get(id=id)
    if uname == article.author.name:
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('无权删除此篇文章')


def article_update(request, id):  # 这个拿的文章id 误认为user id了
    u_id = request.session.get('user_id')
    post = ArticlePost.objects.get(id=id)
    if not u_id == post.author_id:
        return HttpResponse('无权修改文章')
    article =  ArticlePost.objects.get(id=id)
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if  article_post_form.is_valid():
            article.title = request.POST.get('title')
            article.body = request.POST.get('body')
            article.category = article_post_form.cleaned_data.get('category')
            # 删除原来的标签
            old_tag = article.tag.all()
            article.tag.remove(*old_tag)
            # 这个删除了原来的标签
            for i in article_post_form.cleaned_data.get('tag'):
                article.tag.add(i)
            article.save()
            return redirect('article:article_detail',id=id)
        else:
            return HttpResponse('输入数据有误')

    else:
        article_post_form = ArticlePostForm()
        # context = {
        #     'article':article,
        #     # 'article_post_form':article_post_form,
        # }
        return render(request, 'article/update.html', locals())

def article_search(request):
    search = request.POST.get('search')
    articles = ArticlePost.objects.filter(Q(title__icontains=search)|Q(body__icontains=search)).order_by('-views')
    context={
        'articles':articles,
        'search':search
    }
    return render(request, 'article/search.html',context)

def article_views(request):
    current_page = request.GET.get('page')
    all_count =ArticlePost.objects.all().count()
    page_info = page.PageInfo(current_page, all_count, 5,order='-views',category=None,year=None,month=None,tag=None)
    article_list = ArticlePost.objects.all().order_by('-views')

    article_list = article_list[page_info.start():page_info.end()]
    new_article_list = ArticlePost.objects.all()[0:3]
    r = get_redis_connection()
    article_id_list = r.lrange(request.session.get('user_name'), 0, -1)
    redis_lists = []
    for i in article_id_list:
        redis_lists.append(ArticlePost.objects.get(id=i))


    context  ={
        'articles': article_list,
        'page_info':page_info,
        'new_article_list':new_article_list,
        'redis_lists':redis_lists,
    }

    return render(request, 'article/article_views.html', context)

def article_file(request, year, month):
    current_page = request.GET.get('page')
    all_count = ArticlePost.objects.filter(created__year=year,created__month=month).count() #归档下的
    page_info = page.PageInfo(current_page, all_count, 5,order=None,category=None, year=year,month=month,tag=None)
    article_list = ArticlePost.objects.filter(created__year=year,created__month=month)
    article_list = article_list[page_info.start():page_info.end()]
    new_article_list = ArticlePost.objects.all()[0:3]
    r = get_redis_connection()
    article_id_list = r.lrange(request.session.get('user_name'), 0, -1)
    redis_lists = []
    for i in article_id_list:
        redis_lists.append(ArticlePost.objects.get(id=i))

    context  ={
        'articles': article_list,
        'page_info':page_info,
        'new_article_list':new_article_list,
        'redis_lists':redis_lists,
    }

    return render(request, 'article/file.html', context)

def article_category_posts(request, id):
    current_page = request.GET.get('page')
    obj = Category.objects.get(id=id)
    all_count = obj.articlepost_set.all().count() #这也是修改了分类下的所有文章数目
    article_list = obj.articlepost_set.all()
    page_info = page.PageInfo(current_page, all_count, 5,order=None,category=id,year=None,month=None,tag=None)
    article_list = article_list[page_info.start():page_info.end()]
    new_article_list = ArticlePost.objects.all()[0:3]
    r = get_redis_connection()
    article_id_list = r.lrange(request.session.get('user_name'), 0, -1)
    redis_lists = []
    for i in article_id_list:
        redis_lists.append(ArticlePost.objects.get(id=i))

    context  ={
        'articles': article_list,
        'page_info':page_info,
        'new_article_list':new_article_list,
        'redis_lists':redis_lists,
    }

    return render(request, 'article/category_posts.html', context)

def article_tag_posts(request, id):
    current_page = request.GET.get('page')
    obj = Tag.objects.get(id=id)
    all_count=obj.articlepost_set.all().count() # 这修改的是标签下所有文章的数目
    article_list = obj.articlepost_set.all()
    page_info = page.PageInfo(current_page, all_count, 5,order=None,category=None,year=None,month=None,tag=id)

    article_list = article_list[page_info.start():page_info.end()]
    new_article_list = ArticlePost.objects.all()[0:3]
    r = get_redis_connection()
    article_id_list = r.lrange(request.session.get('user_name'), 0, -1)
    redis_lists = []
    for i in article_id_list:
        redis_lists.append(ArticlePost.objects.get(id=i))

    context  ={
        'articles': article_list,
        'page_info':page_info,
        'new_article_list':new_article_list,
        'redis_lists':redis_lists,
    }

    return render(request, 'article/tag_posts.html', context)




