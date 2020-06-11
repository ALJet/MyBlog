from blog.user.models import User, CheckCode, UserRelationship
from blog.models import Topic, Article, UserFollowArticle, UserCollectArticle, create_answer_abstract, Comment, Vote
from rest_framework.serializers import ModelSerializer

#
# class ArticleForCommentSerializer(ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['id']
#
#
# class ArticleSerializer(ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
#
#
#
# class UserProfileSerializer(ModelSerializer):
#     user_vote_article = ArticleForCommentSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class UserSerializer(ModelSerializer):
#     profile = UserProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'username',
#             'password',
#             'profile',
#         ]
#
#
# class AnswerSerializer(ModelSerializer):
#     author = UserProfileSerializer()
#
#     class Meta:
#         model = Article
#         fields = ['id',  'author', 'user_vote', 'abstract', 'like_counts'
#             , 'answer_comments', 'comment_counts', 'create_time']
#
#
# class AnswerDetailSerializer(ModelSerializer):
#     author = UserProfileSerializer()
#     question = OnlyQuestionSerializer()
#
#     class Meta:
#         model = Answer
#         fields = ['id', 'question', 'author', 'user_vote', 'content', 'like_counts'
#             , 'answer_comments', 'comment_counts', 'create_time']
#
#
#
# class TopicSerializer(ModelSerializer):
#     class Meta:
#         model = Topic
#         fields = '__all__'
#
#
# class CommentUserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'avatar']
#
#
# class ReplyCommentSerializer(ModelSerializer):
#     comment_user = CommentUserSerializer()
#     parent = CommentUserSerializer()
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent']
#         depth = 1
#
#
# class ChildCommentSerializer(ModelSerializer):
#     comment_user = CommentUserSerializer()
#     reply_to = ReplyCommentSerializer()
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent', 'reply_to']
#         depth = 1
#
#
# class CommentSerializer(ModelSerializer):
#     comment_user = CommentUserSerializer()
#     belong_to = ArticleSerializer()
#     child_comments = ChildCommentSerializer(many=2, )
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'belong_to', 'child_comments']
#         depth = 1