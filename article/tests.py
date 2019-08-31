from django.test import TestCase
import datetime
from django.utils import timezone
from article.models import ArticlePost
from userprofile.models import User
# Create your tests here.

class ArticlePostModelTests(TestCase):
    def test_was_created_recently_with_future_article(self):
        user = User(name='user', password='test_password')
        user.save()

        future_article = ArticlePost(
            author=user,
            title = 'test',
            body='test',
            created=timezone.now()+datetime.timedelta(days=30)
        )
        self.assertIs(future_article.was_created_recently(), False)

    def test_was_created_recently_with_seconds_before_article(self):
        user = User(name='user1', password='test_password')
        user.save()
        seconds_before_article = ArticlePost(
            author = user,
            title = 'test1',
            body = 'test1',
            created=timezone.now() - datetime.timedelta(seconds=45)
        )
        self.assertIs(seconds_before_article.was_created_recently(),True)

    def test_was_created_recently_with_hours_before_article(self):
        user = User(name='user2', password='test_password')
        user.save()
        hours_before_article = ArticlePost(
            author=user,
            title='test2',
            body='test2',
            created=timezone.now() - datetime.timedelta(hours=3)
        )
        self.assertIs(hours_before_article.was_created_recently(), False)

    def test_was_created_recently_with_days_before_article(self):
        # 若文章创建时间为几天前，返回 False
        user = User(name='user3', password='test_password')
        user.save()
        months_before_article = ArticlePost(
            author=user,
            title='test3',
            body='test3',
            created=timezone.now() - datetime.timedelta(days=5)
            )
        self.assertIs(months_before_article.was_created_recently(), False)

