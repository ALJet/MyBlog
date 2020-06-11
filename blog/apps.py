from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = "博客文章管理"


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = "用户管理"
