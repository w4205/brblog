from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

web = Blueprint('web', __name__)


@web.app_errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@web.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@web.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@web.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/400.html', description=e.description), 400


from app.web import blog, auth, admin