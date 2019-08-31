from flask import request, current_app, render_template, url_for, flash, \
    redirect, abort, make_response
from flask_login import current_user
from sqlalchemy import desc

from app import Category, Comment, db
from app.forms.comment import AdminCommentForm, CommentForm
from app.libs.email import send_email
from app.libs.redirect_next import redirect_next
from app.models.post import Post
from . import web

@web.route('/')
def index():
    page = request.args.get('page',default=1,type=int)
    per_page = current_app.config['BRBLOG_POST_PER_PAGE']
    pagination = Post.query.filter_by(status=1).order_by(
                 Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@web.route('/about')
def about():
    return render_template('blog/about.html')

# @web.route('/post/<int:post_id>')
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     page = request.args.get('page',default=1, type=int)
#     per_page = current_app.config['BRBLOG_COMMENT_PER_PAGE']
#     pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(
#         Comment.timestamp,desc()).paginate(page, per_page)
#     comments = pagination.items
#
#
#     return render_template('blog/post.html',comments=comments,pagination=pagination)
#
@web.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.filter_by(
        status=1,id=category_id).first_or_404()
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['BRBLOG_POST_PER_PAGE']
    pagination = Post.query.filter_by(status=1).with_parent(category).order_by(
        Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category,
                           pagination=pagination, posts=posts)



@web.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.filter_by(
        status=1,id=post_id).first_or_404()
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['BRBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(
        reviewed=True).order_by(Comment.timestamp.asc()).paginate(page,per_page)
    comments = pagination.items

    if current_user.is_authenticated:    # 已经登录使用管理员表单
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['MAIL_USERNAME']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:   # 未登录使用普通表单
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        # 如果是回复评论
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_email(replied_comment.email, '有新回复', 'email/replied.html',
                       post=post, comment=comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # 管理员直接提交评论
            flash('回复成功', 'success')
        else:
            flash('感谢回复,您的评论稍后显示', 'info')
            send_email(current_app.config['MAIL_USERNAME'], '有新评论',
                       'email/commented.html', post=post, comment=comment)  # 非管理员评论会发送邮件给管理者
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination,
                           form=form, comments=comments)


@web.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('当前文章未开放评论', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(url_for('.show_post', post_id=comment.post_id,
                    reply=comment_id,author=comment.author) + '#comment-form')


@web.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BRBLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_next())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
