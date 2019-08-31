from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy



class SQLAlchemy(_SQLAlchemy):
    """
    增加自动 commit 上下文管理器,并且程序出错自动 rollback
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()    # 数据库回滚
            raise e

db = SQLAlchemy()


class Base(db.Model):

    # 基类不创建数据库表
    __abstract__ = True

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # 软删除状态,0=删除,1=未删除
    status = db.Column(db.SmallInteger,default=1)

    def delete(self):
        with db.auto_commit():
            self.status = 0

