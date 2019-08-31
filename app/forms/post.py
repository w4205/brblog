from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from app.models.category import Category


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(message='标题不能为空'),
                        Length(1, 60, message='长度必须在 1-60 字符之间')])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        # 下拉选项标签通过 choices 指定
        # 依赖 flask 上下文才能获取到 category 对象
        # 也可以实例化 category 时对 choices 赋值
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]
