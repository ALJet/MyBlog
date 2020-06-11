from DjangoUeditor.models import UEditorField
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.
from blog.user.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Topic(models.Model):
    '''话题分类'''
    name = models.CharField('话题', max_length=40)
    description = models.CharField('话题描述', max_length=200, null=True,
                                   blank=True)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    image = models.ImageField('话题图片', upload_to='image/%Y/%m/',
                              default='image/default_topic.jpg', null=True,
                              blank=True)

    users = models.ManyToManyField(User, blank=True, verbose_name='用户话题')

    class Meta:
        verbose_name = '话题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_user_nums(self):
        '''获取关注者数量'''
        return self.users.count()


class Article(models.Model):
    '''文章模型'''

    title = models.CharField('文章标题', max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               verbose_name='文章作者', related_name='article_author')
    topics = models.ForeignKey(Topic, blank=True, null=True, verbose_name='话题', related_name='article_topics',
                               on_delete=models.SET(get_sentinel_user))
    description = models.CharField('文章简介', max_length=200, default='.........')
    content = UEditorField(verbose_name="文章内容", imagePath="article/images/", width=1000, height=300,
                           filePath="article/files/", default='')
    # content = models.TextField('文章内容', null=True, blank=True)

    pub_time = models.DateTimeField('发布时间', auto_now_add=True)
    recommend = models.BooleanField('是否推荐', default=False)
    read_nums = models.IntegerField('浏览量', default=0)
    is_anonymous = models.BooleanField('匿名文章', default=False)
    # 喜欢文章的人
    user_vote = models.ManyToManyField(to=User, verbose_name='喜欢文章的人', related_name='user_vote_article', blank=True,
                                       )
    like_counts = models.IntegerField('赞', default=0)
    dislike_counts = models.IntegerField('踩', default=0)
    comment_counts = models.IntegerField('评论数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def get_topic_name(self):
        '''获取话题名'''
        return self.topics.first().name

    def get_follow_nums(self):
        '''获取关注者数量'''
        return self.userfollowquestion_set.count()


class UserFollowArticle(models.Model):
    '''用户关注文章模型'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name='关注文章')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户关注文章'
        verbose_name_plural = verbose_name


class UserCollectArticle(models.Model):
    '''用户收藏文章模型'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name='收藏文章')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户收藏文章'
        verbose_name_plural = verbose_name


# 取文章前200字符做摘要
@receiver(post_save, sender=Article)
def create_answer_abstract(sender, instance, created, **kwargs):
    if created:
        content = instance.content
        instance.abstract = content[:200]
        instance.save()


class Comment(models.Model):
    '''评论表'''
    comment_user = models.ForeignKey(to=User, related_name='comment_author', on_delete=models.CASCADE,
                                     verbose_name='评论者')
    user_ip = models.CharField(null=True, blank=True, max_length=30, verbose_name='用户IP')
    belong_to = models.ForeignKey(to=Article, related_name='answer_comments', on_delete=models.CASCADE,
                                  verbose_name='博客文章作者')
    # 父评论
    parent = models.ForeignKey(to='self', related_name='child_comments', null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name='父评论')
    # 回复对象
    reply_to = models.ForeignKey(to='self', related_name='who_reply', null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='回复对象')
    # content = models.TextField(null=True, blank=True, verbose_name='评论内容')
    content = UEditorField(verbose_name="评论内容", imagePath="comment/images/", width=1000, height=300,
                           filePath="comment/files/", default='')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='评论时间')

    def __str__(self):
        return self.comment_user.nickname

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class Vote(models.Model):
    '''投票表'''
    owner = models.ForeignKey(to=User, related_name='user_vote', on_delete=models.CASCADE, verbose_name='作者')
    give_to = models.ForeignKey(to=Article, related_name='vote', on_delete=models.CASCADE, verbose_name='投票者')
    # 1是未作选择，2是赞同，3是反对
    vote = models.IntegerField(default=1, verbose_name='投票数')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='投票时间')

    class Meta:
        verbose_name = '用户投票'
        verbose_name_plural = verbose_name
