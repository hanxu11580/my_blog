from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [

    path(r'article-list/', views.article_list, name='article_list'),
    path(r'article-detail/<int:id>/', views.article_detail, name ='article_detail'),
    path(r'article-create/', views.article_create, name='article_create'),
    path(r'article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path(r'article-update/<int:id>/', views.article_update, name='article_update'),
    path(r'article-search/', views.article_search, name='article_search'),
    path(r'article-views/', views.article_views, name='article_views'),
    path(r'article-file/<int:year>/<int:month>/', views.article_file, name='article_file'),
    path(r'article-category-posts/<int:id>/', views.article_category_posts, name='article_category_posts'),
    path(r'article-tag-posts/<int:id>/', views.article_tag_posts, name='article_tag_posts')

]