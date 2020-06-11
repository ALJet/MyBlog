from blog.user.models import User, CheckCode, UserRelationship
from blog.models import Topic, Article, UserFollowArticle, UserCollectArticle, create_answer_abstract, Comment, Vote
from rest_framework.serializers import ModelSerializer


class ArticleForCommentSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
        depth = 1
        # fields = [
        #     'id',
        #     'name',
        #     'description',
        #     'add_time',
        #     'image',
        #     'users',
        # ]


class UserArticleSerializer(ModelSerializer):
    article_author = ArticleForCommentSerializer()

    class Meta:
        model = User
        fields = '__all__'


class TopicArticleSerializer(ModelSerializer):
    article_topics = TopicSerializer()

    class Meta:
        model = Topic
        # fields = '__all__'
        # depth = 1
        fields = [
            'id',
            'name',
            'description',
            'add_time',
            'image',
            'users',
        ]


class UserPartSerializer(ModelSerializer):
    # profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            # 'profile',
            'image',
            'nickname',
            'description',
        ]


class ArticleSerializer(ModelSerializer):
    author = UserArticleSerializer()
    topics = TopicSerializer()

    class Meta:
        model = Article
        fields = ['id', 'author', 'topics', 'title', 'description', 'content', 'pub_time'
            , 'recommend', 'read_nums', 'is_anonymous', 'like_counts', 'dislike_counts', 'comment_counts']


class ArticleDetailSerializer(ModelSerializer):
    article_author = UserArticleSerializer()
    article_topics = TopicSerializer()

    class Meta:
        model = Article
        fields = ['id', 'author', 'topics', 'title', 'description','content', 'pub_time'
            , 'recommend', 'read_nums', 'is_anonymous', 'like_counts', 'dislike_counts', 'comment_counts']


class CommentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'image']


class ReplyCommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    parent = CommentUserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent']
        depth = 1


class ChildCommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    reply_to = ReplyCommentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent', 'reply_to']
        depth = 1


class CommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    belong_to = ArticleSerializer()
    child_comments = ChildCommentSerializer(many=2, )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'belong_to', 'child_comments']
        depth = 1
