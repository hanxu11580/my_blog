from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# 拿到一个有parent_comment的评论，需要去找到它的父评论， 并添加到其中
def tree_search(comment_dic, comment_obj):
    for k,v in comment_dic.items():
        '''
            如果找到了，拿到一个评论里面有一个字段parent，然后将会找所有的评论，去和其他评论的主键匹配，匹配成功代表着这条评论是其的子评论，那么将加到键k下，[comment_obj]={}这个是留下字典结构方便以后将继续添加子评论
        '''
        if k == comment_obj.parent_comment:
            comment_dic[k][comment_obj] = {}
            return
        else:
            '''
                如果没找到，去下一层去找
            '''
            tree_search(comment_dic[k], comment_obj)


# 下面是遍历子评论，并将子评论拼接,遍历主要是通过递归
def generate_comment_html(sub_comment_dic, margin_left):
    html = ""
    for k,v in sub_comment_dic.items():
        html += "<div style='margin-left:%spx' class='comment-node'>" % margin_left + "<p><strong style='color: pink'>"+k.user.name+"</strong> 于<span style='color: #66afe9'>"+str(k.created.year)+'-'+str(k.created.month)+'-'+str(k.created.day)+"</span> 回复："+k.parent_comment.user.name+"</p><pre style='font-family: inherit; font-size: 1em;'>"+k.body+"<a href='/comment/hf-comment/"+"?par="+str(k.id)+"&article_id="+str(k.article.id)+"'>回复他</a>"+"</pre>" + "</div>"
        # html += "<div class='comment-node' style='margin-left:%spx'>" % margin_left+"<hr><p><strong style='color: pink'>"+k.user.name+"</strong> 于<span style='color: #66afe9'>"+str(k.created.year)+'-'+str(k.created.month)+'-'+str(k.created.day)+"</span> 时说：</p><pre style='font-family: inherit; font-size: 1em;'>"+k.body+"</pre>" +"</div>"
        # 拿出评论的内容并且拼接在html中
        if  v:
            html += generate_comment_html(v, margin_left+30)
    return html
        # 如果子评论在下面还有评论，那么v将会存在值，并且显示将会向右移动15像素，一个子评论及其下面的评论遍历完，将会遍历下一条子评论

'''
    下面主要是如何构造一个树形字典
'''
@register.simple_tag
def build_comment_tree(comment_list): # comment_list是从数据库取到的queryset列表对象，遍历它将会得到评论对象
    comment_dic = {}
    for comment_obj in comment_list:
        if comment_obj.parent_comment is None:
            comment_dic[comment_obj]={}
            # 将无父评论的评论对象放到字典中并设置{}空字典，为以后加子评论用
            
        else:
            tree_search(comment_dic, comment_obj)
    # 字典构造完后，进行html拼接
    html = "<div class='comment-bos'>"
    margin_left = 0
    for k,v in comment_dic.items():
        html+="<div class='comment-node'>"+"<hr><p><strong style='color: pink'>"+k.user.name+"</strong> 于<span style='color: #66afe9'>"+str(k.created.year)+str(k.created.month)+str(k.created.day)+"</span> 时说：</p><pre style='font-family: inherit; font-size: 1em;'>"+k.body+"<a href='/comment/hf-comment/"+"?par="+str(k.id)+"&article_id="+str(k.article.id)+"'>回复他</a>"+"</pre>"+"</div>"
        html+=generate_comment_html(v,margin_left+30)
    html+="</div>"
    return mark_safe(html)





