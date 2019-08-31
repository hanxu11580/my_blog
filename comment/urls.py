from django.urls import path
from comment import views

app_name = 'comment'

urlpatterns =[
    path(r'post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # 上方是原有的url用户处理一级评论，不用删除
    path(r'hf-comment/', views.hf_comment, name='hf_comment'),


]