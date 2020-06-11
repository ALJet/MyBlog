import xadmin
from xadmin import views
from .models import Topic, Article, UserFollowArticle, UserCollectArticle, Comment, Vote


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客后台系统"
    site_footer = "liang09007@163.com"
    # menu_style = "accordion"


class TopicAdmin(object):
    list_display = ['name', 'description', 'add_time', 'image', ]
    search_fields = ['name', 'description', 'add_time', ]
    list_filter = ['name', 'description', 'add_time', ]


class ArticleAdmin(object):
    list_display = ['title', 'author', 'description', 'topics', 'pub_time', 'recommend', 'read_nums', 'is_anonymous', ]
    search_fields = ['title', 'author', 'topics', 'pub_time']
    list_filter = ['title', 'author', 'content', 'topics', 'pub_time', ]
    style_fields = {"content": "ueditor"}


class UserFollowArticleAdmin(object):
    list_display = ['user', 'article', 'add_time', ]
    search_fields = ['user', 'article', 'add_time', ]
    list_filter = ['user', 'article', 'add_time', ]


class UserCollectArticleAdmin(object):
    list_display = ['user', 'article', 'add_time', ]
    search_fields = ['user', 'article', 'add_time', ]
    list_filter = ['user', 'article', 'add_time', ]


class CommentAdmin(object):
    list_display = ['comment_user', 'content','user_ip', 'belong_to', 'parent', 'reply_to', 'create_time', ]
    search_fields = ['comment_user','content', 'create_time', ]
    list_filter = ['comment_user', 'parent', 'reply_to', 'create_time', ]
    style_fields = {"content": "ueditor"}


class VoteAdmin(object):
    list_display = ['owner', 'give_to', 'vote', 'create_time', ]
    search_fields = ['owner', 'give_to', 'vote', 'create_time', ]
    list_editable = ["vote", ]
    list_filter = ['owner', 'give_to', 'vote', 'create_time', ]


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(UserCollectArticle, UserCollectArticleAdmin)
xadmin.site.register(UserFollowArticle, UserFollowArticleAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Vote, VoteAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
