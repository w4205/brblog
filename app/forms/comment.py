from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, URL, Optional, Email


class CommentForm(FlaskForm):
    author = StringField('昵称(必填)', validators=[DataRequired(),
                         Length(2, 30, message='昵称必须在 2-30 个字符之间')])
    email = StringField('邮箱(必填)', validators=[DataRequired(),
                        Email(message='请输入正确 email 地址'), Length(1, 254)])
    site = StringField('网站', validators=[Optional(), URL(), Length(0, 254)])
    body = TextAreaField('发表评论', validators=[DataRequired()])
    submit = SubmitField('提交评论')

class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()