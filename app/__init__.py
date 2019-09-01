import click
from flask import Flask
from flask_login import current_user

from app.libs.extentions import bootstrap, csrf, ckeditor, mail, moment, login_manager
from app.models import db
from app.models.admin import Admin
from app.models.category import Category
from app.models.comment import Comment
from app.models.link import Link
from app.models.post import Post
from app.web import web


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')

    app.register_blueprint(web)
    register_extensions(app)
    register_template_contaxt(app)
    register_commands(app)

    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_template_contaxt(app):
    @app.context_processor
    def template_context():
        """向模板上下文中添加 admin 和 category 对象,以便取到博客标题分类等数据,
        传入 current_user
        可避免每个视图函数都传入"""
        admin = Admin.query.first()
        categories = Category.query.filter_by().order_by(Category.name).all()
        links = Link.query.filter_by().order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)

def register_commands(app):
    @app.cli.command()      # 注册 flask 命令行
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """初始化数据库"""
        if drop:
            click.confirm('这个操作会删除数据库,继续吗?', abort=True)
            db.drop_all()
            click.echo('删除数据库')
        db.create_all()
        click.echo('初始化数据库成功')

    @app.cli.command()
    @click.option('--username', prompt=True, help='管理员账号')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='管理员密码')
    def init(username, password):
        """初始化数据库 admin 分类"""
        click.echo('初始化数据库中...')
        db.create_all()

        with db.auto_commit():
            admin = Admin.query.first()
            if admin is not None:
                click.echo('管理员账号已存在,更新中...')
                admin.username = username
                admin.set_password(password)
            else:
                click.echo('创建默认管理员数据中...')
                admin = Admin(
                    username=username,
                    blog_title='Br Blog',
                    blog_sub_title="Genius only means hard-working all one's life.",
                    name='Jack Zhang',
                    about='''永不放弃是人生要成功的一大因素，
            只要能够坚持，
            锲而不舍，
            终会到达成功的彼岸的。'''
                )
                admin.set_password(password)
                db.session.add(admin)

            category = Category.query.first()
            if category is None:
                click.echo('创建默认分类...')
                category = Category(name='Default')
                db.session.add(category)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """生成虚拟数据"""
        from app.libs.faker import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('生成管理员数据...')
        fake_admin()

        click.echo('生成 %d 个分类...' % category)
        fake_categories(category)

        click.echo('生成 %d 篇文章...' % post)
        fake_posts(post)

        click.echo('生成 %d 条评论...' % comment)
        fake_comments(comment)

        click.echo('生成友情链接...')
        fake_links()

        click.echo('完成.')
