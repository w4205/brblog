from flask import flash, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import db, Post, Category, Comment, Link
from app.forms.admin import SettingForm
from app.forms.link import LinkForm
from app.forms.category import CategoryForm
from app.forms.post import PostForm
from app.libs.redirect_next import redirect_next
from . import web

@web.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('设置已更新', 'success')
        return redirect(url_for('web.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@web.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', default=1, type=int)
    pagination = Post.query.filter_by(status=1).order_by(
        Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'BRBLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page,
                           pagination=pagination, posts=posts)


@web.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('发表成功.', 'success')
        return redirect(url_for('web.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@web.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('评论已关闭.', 'success')
    else:
        post.can_comment = True
        flash('评论已打开', 'success')
    db.session.commit()
    return redirect_next()


@web.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('web.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@web.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.delete()
    # db.session.delete(post)
    # db.session.commit()
    flash('文章已删除', 'success')
    return redirect_next()


@web.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', default=1, type=int)
    per_page = current_app.config['BRBLOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(status=1).filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(status=1, from_admin=True)
    else:
        filtered_comments = Comment.query.filter_by(status=1)

    pagination = filtered_comments.order_by(
                 Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html',
                           comments=comments, pagination=pagination)


@web.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('已审核通过', 'success')
    return redirect_next()


@web.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # db.session.delete(comment)
    comment.delete()
    db.session.commit()
    flash('已成功删除', 'success')
    return redirect_next()


@web.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@web.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('已创建分类', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@web.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能修改默认分类', 'warning')
        return redirect(url_for('web.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('已修改分类', 'success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@web.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能删除默认分类', 'warning')
        return redirect(url_for('web.index'))
    category.delete()
    flash('分类已删除', 'success')
    return redirect(url_for('.manage_category'))


@web.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


@web.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('已新建链接', 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


@web.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('已修改链接.', 'success')
        return redirect(url_for('.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@web.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    # db.session.delete(link)
    link.delete()
    db.session.commit()
    flash('链接已删除', 'success')
    return redirect(url_for('.manage_link'))