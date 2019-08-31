from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),
                            Length(2, 20,message='长度必须在 2-20 字符之间')])
    password = PasswordField('密码', validators=[DataRequired(),
                            Length(6, 128, message='密码必须大于 6 个字符')])
    remember = BooleanField('记住登录信息')
    submit = SubmitField('登录')

class SettingForm(FlaskForm):
    name = StringField('昵称', validators=[DataRequired(),
                        Length(1, 70, message='长度必须在 1-70 字符之间')])
    blog_title = StringField('博客标题', validators=[DataRequired(),
                              Length(1, 20,message='长度必须在 1-20 字符之间')])
    blog_sub_title = StringField('副标题', validators=[DataRequired(),
                                 Length(1, 100,message='长度必须在 1-100 字符之间')])
    about = CKEditorField('关于', validators=[DataRequired()])
    submit = SubmitField('保存设置')

