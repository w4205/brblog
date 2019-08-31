from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL


class LinkForm(FlaskForm):
    name = StringField('网站名', validators=[DataRequired(),
                        Length(1, 30,message='网站名必须在 1-30 个字符之间')])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField('保存')