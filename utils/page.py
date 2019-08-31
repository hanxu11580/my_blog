class PageInfo(object):
    def __init__(self, current_page, all_count, per_page, order, category,year,month,tag,show_page=7):
        try: # 如果页码为非法的则会显示到第一页
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page
        self.order = order
        self.category = category
        self.year = year
        self.month = month
        self.tag = tag

        a, b = divmod(all_count, per_page) # 所有的页码总数/用于下方pager方法
        if b:
            a = a + 1
        self.all_pager = a
        self.show_page = show_page


    def start(self):
        return (self.current_page -1)*self.per_page
    def end(self):
        return self.current_page*self.per_page


    def pager(self):
        page_list = []
        half = int((self.show_page-1)/2)
        if self.all_pager <= self.show_page:
            begin = 1
            stop = self.all_pager+1
        else:  #现在是总也是大于7
            if self.current_page <= half:
                begin = 1
                stop = self.current_page + half + 1
            else:
                if self.current_page+half > self.all_pager:
                    begin = self.current_page - half
                    stop = self.all_pager + 1

        if self.category:
            if self.current_page > 1:
                pre = "<li><a href='/article/article-category-posts/%s/?page=%s'>上一页</a></li>" % (self.category, self.current_page - 1)
                page_list.append(pre)

            for i in range(begin, stop):
                if i == self.current_page:
                    temp = "<li class='active'><a href='/article/article-category-posts/%s/?page=%s'>%s</a></li>" % (self.category, i, i)
                else:
                    temp = "<li><a href='/article/article-category-posts/%s/?page=%s'>%s</a></li>" % (self.category, i, i)
                page_list.append(temp)

            if self.current_page < self.all_pager:
                next = "<li><a href='/article/article-category-posts/%s/?page=%s'>下一页</a></li>" % (self.category, self.current_page + 1)
                page_list.append(next)

        elif self.year:
            if self.current_page > 1:
                pre = "<li><a href='/article/article-file/%s/%s/?page=%s'>上一页</a></li>" % (self.year, self.month,self.current_page - 1)
                page_list.append(pre)

            for i in range(begin, stop):
                if i == self.current_page:
                    temp = "<li class='active'><a href='/article/article-file/%s/%s/?page=%s'>%s</a></li>" % (self.year,self.month, i, i)
                else:
                    temp = "<li><a href='/article/article-file/%s/%s/?page=%s'>%s</a></li>" % (self.year,self.month, i, i)
                page_list.append(temp)

            if self.current_page < self.all_pager:
                next = "<li><a href='/article/article-file/%s/%s/?page=%s'>下一页</a></li>" % (self.year,self.month, self.current_page + 1)
                page_list.append(next)

        elif self.tag:
            if self.current_page > 1:
                pre = "<li><a href='/article/article-tag-posts/%s/?page=%s'>上一页</a></li>" % (self.tag, self.current_page - 1)
                page_list.append(pre)

            for i in range(begin, stop):
                if i == self.current_page:
                    temp = "<li class='active'><a href='/article/article-tag-posts/%s/?page=%s'>%s</a></li>" % (self.tag, i, i)
                else:
                    temp = "<li><a href='/article/article-tag-posts/%s/?page=%s'>%s</a></li>" % (self.tag, i, i)
                page_list.append(temp)

            if self.current_page < self.all_pager:
                next = "<li><a href='/article/article-tag-posts/%s/?page=%s'>下一页</a></li>" % (self.tag, self.current_page + 1)
                page_list.append(next)


        else:

            if self.current_page > 1:
                pre = "<li><a href='/article/article-list/?page=%s&order=%s'>上一页</a></li>" % (self.current_page - 1,self.order)
                page_list.append(pre)

            for i in range(begin, stop):
                if i == self.current_page:
                    temp = "<li class='active'><a href='/article/article-list/?page=%s&order=%s'>%s</a></li>" % (i, self.order,i)
                else:
                    temp = "<li><a href='/article/article-list/?page=%s&order=%s'>%s</a></li>" % (i, self.order,i)
                page_list.append(temp)

            if self.current_page < self.all_pager:
                next = "<li><a href='/article/article-list/?page=%s&order=%s'>下一页</a></li>" % (self.current_page + 1,self.order)
                page_list.append(next)




        return ''.join(page_list)




