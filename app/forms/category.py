from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models.category import Category


class CategoryForm(FlaskForm):
    name = StringField('分类名', validators=[DataRequired(),
                        Length(1, 10, message='长度必须在 1-10 个字符之间')])
    submit = SubmitField('保存')

    def validate_name(self, category):
        if Category.query.filter_by(name=category.data).first():
            raise ValidationError('分类已经存在')