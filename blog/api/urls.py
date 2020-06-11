from django.urls import path, include
from .views import user_info, user_info_detail, user_now, article, article_id, register, user_login, user_vote, \
    edit_user, comment, child_comments, topic, user_article_like, user_article, search, article_detail, getComment

urlpatterns = [
    path('api/users/', user_info),
    path('api/user/<int:user_loginuser_id>/', user_info_detail),
    path('api/users/now/', user_now),
    path('api/register/', register, name='register'),
    path('api/login/', user_login),
    path('api/edit_user/<int:user_id>/', edit_user),
    path('api/articles/', article),
    path('api/articles/<int:article_id>/', article_detail),
    path('api/comments/', comment),
    path('api/child_comments/<int:comment_id>/', child_comments),
    path('api/topics/', topic),
    path('api/user_vote/', user_vote),
    path('api/user/article_like/', user_article_like),
    path('api/user/article/', user_article),
    path('api/search/', search),
    path('api/<int:user_id>/comments/', getComment),

]
