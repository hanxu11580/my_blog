from django import template
from article import models
from django.db.models.aggregates import Count
from django.core.cache import cache

register = template.Library()
'''
回档
'''
def file_data():
    key = 'file'
    if cache.has_key(key):
        return cache.get(key)
    else:
        cache.set(key, models.ArticlePost.objects.dates('created', 'month', order='DESC'), 43200) #回档一天更新2次
'''
分类
'''
def category_data():
    key = 'category'
    if cache.has_key(key):
        return cache.get(key)
    else:
        cache.set(key, models.Category.objects.annotate(num_posts=Count('articlepost')),2880)#2个小时更新一次

'''
标签
'''
def tag_data():
    key = 'tag'
    if cache.has_key(key):
        return cache.get(key)
    else:
        cache.set(key, models.Tag.objects.all(),2880)
@register.simple_tag
def file():
    # return models.ArticlePost.objects.dates('created', 'month', order = 'DESC')
    return file_data()
@register.simple_tag
def categorys():
    # return models.Category.objects.annotate(num_posts=Count('articlepost'))
    # 这个很好用,不光会返回所有的分类,而且会统计每个分类下的文章数
    return category_data()

@register.simple_tag
def tags():
    # return models.Tag.objects.all()
    return tag_data()