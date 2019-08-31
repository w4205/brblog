from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_wtf import CSRFProtect


bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from app import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'web.login'
login_manager.login_message_category = 'warning'