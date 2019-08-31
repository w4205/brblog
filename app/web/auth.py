from flask import url_for, flash, render_template
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from . import web
from app.models.admin import Admin
from app.forms.admin import LoginForm
from app.libs.redirect_next import redirect_next


@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来', 'info')
                return redirect_next()
            flash('用户名或密码错误', 'warning')
        else:
            flash('还没有生成账户', 'warning')
    return render_template('auth/login.html', form=form)


@web.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功.', 'info')
    return redirect_next()
