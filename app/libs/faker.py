import random

from faker import Faker

from app.models import db
from app.models.admin import Admin
from app.models.category import Category
from app.models.comment import Comment
from app.models.link import Link
from app.models.post import Post

faker = Faker()

def fake_admin():
    with db.auto_commit():
        data = Admin(
            username='admin',
            blog_title='Br Blog',
            blog_sub_title = "Genius only means hard-working all one's life.",
            name = 'Jack Zhang',
            about = '''永不放弃是人生要成功的一大因素，
            只要能够坚持，
            锲而不舍，
            终会到达成功的彼岸的。'''
        )
        data.set_password('adminadmin')
        db.session.add(data)


def fake_categories(nums=5):
    with db.auto_commit():
        # 优先生成默认分类
        data = Category(name='default')
        db.session.add(data)
        for i in range(nums):
            data = Category(name=faker.word())
            db.session.add(data)


def fake_posts(nums=50):
    with db.auto_commit():
        for i in range(nums):
            data = Post(
                title=faker.sentence(),
                body=faker.text(2000),
                category=Category.query.get(
                    random.randint(1, Category.query.count())),
                timestamp=faker.date_time_this_year()
            )
            db.session.add(data)

            
def fake_comments(nums=500):
    with db.auto_commit():
        for i in range(nums):
            # 已审核文章评论
            data = Comment(
                author=faker.name(),
                email=faker.email(),
                site=faker.url(),
                body=faker.sentence(),
                timestamp=faker.date_time_this_year(),
                reviewed=True,
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(data)


        for i in range(int(nums *0.1)):
            # 未审核评论
            data = Comment(
                author=faker.name(),
                email=faker.email(),
                site=faker.url(),
                body=faker.sentence(),
                timestamp=faker.date_time_this_year(),
                reviewed=False,
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(data)
            # 管理员评论
            data = Comment(
                author='张小萌',
                email='mima@example.com',
                site='example.com',
                body=faker.sentence(),
                timestamp=faker.date_time_this_year(),
                from_admin=True,
                reviewed=True,
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(data)


    # 先 commit 评论之后才能生成针对评论的回复
    with db.auto_commit():
        for i in range(int(nums*0.05)):
            data = Comment(
                author=faker.name(),
                email=faker.email(),
                site=faker.url(),
                body=faker.sentence(),
                timestamp=faker.date_time_this_year(),
                reviewed=True,
                replied=Comment.query.get(
                    random.randint(1, Comment.query.count())),
                post=Post.query.get(random.randint(1, Post.query.count()))
            )
            db.session.add(data)


def fake_links():
    with db.auto_commit():
        baidu = Link(name='百度', url='https://www.baidu.com')
        weibo = Link(name='微博', url='https://weibo.com/')
        zhihu = Link(name='知乎', url='http://www.zhihu.com/')
        db.session.add_all([baidu, weibo, zhihu])
