# 引入celery实例对象
from .celery import app as celery_app

__all__ = ('celery_app')
