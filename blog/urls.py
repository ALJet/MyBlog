from django.urls import path
from .views import Index, topic_page, search, topic_detail_page, article_detail, user_articles, test, add_article, \
    user_personal, edit_user, user_comment

urlpatterns = [
    path('', Index),
    path('user/<int:user_id>/', user_personal, name='user_personal'),
    path('user/<int:user_id>/articles/', user_articles, name='user_articles'),
    path('user/<int:user_id>/edit/', edit_user, name='user_edit'),
    path('user/<int:user_id>/comments/', user_comment, name='user_comment'),
    path('index/', Index, name='index'),
    path('topic/', topic_page, name='topic'),
    path('search/', search, name='search'),
    path('article/<int:article_id>/', article_detail, name='article'),
    path('add_article/', add_article, name='add_article'),
    path('test/', test),
]
