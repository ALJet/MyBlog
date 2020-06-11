from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from django.urls import reverse
from rest_framework.response import Response
import base64

from blog.paginator import get_page_list
from blog.user.models import User
from blog.models import Article, Topic, Comment, Vote
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from blog.api.serializers import UserPartSerializer, ArticleSerializer, CommentSerializer, ChildCommentSerializer, \
    TopicSerializer
from django.shortcuts import get_object_or_404
from blog.tasks import send_email


# 返回所有用户信息
@api_view(['GET'])
def user_info(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'people':
            q = request.GET.get('q')
            user_list = User.objects.filter(Q(username__icontains=q))
        else:
            user_list = User.objects.all()
        serializer = UserPartSerializer(user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 返回具体那个用户信息
@api_view(['GET'])
def user_info_detail(request, user_id):
    if request.method == 'GET':
        user_list = User.objects.get(id=user_id)
        serializer = UserPartSerializer(user_list)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 用来判断当前用户身份，返回其信息
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def user_now(request):
    if request.method == 'GET':
        if request.auth:
            request_user = request.user
            serializer = UserPartSerializer(request_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'user_now': 'not_login'}, status=status.HTTP_401_UNAUTHORIZED)


# 注册
@api_view(['GET', 'POST'])
def register(request):
    if request.method == "POST":
        data = request.data
        name = data.get('nickname')
        passwd = data.get('password')
        nickname = data.get('nickname')

        # 手机注册用户
        if 'phone' in data:
            phone = data.get('phone')
            user_exist = User.objects.filter(phone=phone).exists()
            # 手机号被注册
            if user_exist:
                return Response({'msg': '手机号已被注册'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # user_info = User(phone=phone)
                # user_info.set_password(passwd)
                # user_info.save()
                User.objects.create(nickname=nickname, username=name, phone=phone, password=passwd)

                return Response({"msg": '注册成功'}, status=status.HTTP_200_OK)

        # 邮箱注册用户
        elif 'email' in data:
            email = data.get('email')
            user_exist = User.objects.filter(email=email).exists()
            # 邮箱被注册
            if user_exist:
                return Response({'msg': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_info = User(nickname=nickname, username=name, email=email)
                user_info.set_password(passwd)
                user_info.save()
                # User.objects.create(nickname=nickname, username=name, email=email, password=passwd)

                # 生成账户确认签名
                # token = User.generate_confirm_token()
                # 发送账户激活链接邮件
                # send_email.delay(subject='MyBlog账户确认', template='blog/email/user_confirm', to=user_info.email,
                #                  host=request.get_host(), username=user_info.username,
                #                  token=token)

                # 网页显示账户注册成功消息
                # messages.info(request, '账户已注册, 一封账户确认邮件已发往你的邮箱, 请查收')
                return Response({'msg': '注册成功，请点击登录！',
                                 }, status=status.HTTP_200_OK)
        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# 登录
@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        data = request.data
        # print(data)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        # 判断用户信息是否正确
        if not user or not username:
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 用户信息正确生成token
            token, created = Token.objects.get_or_create(user=user)
            auth.login(request, user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


'''修改用户'''


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def edit_user(request, user_id):
    if request.user.id is not None:
        if int(request.user.id) == int(user_id):
            profile = User.objects.get(id=user_id)
            user = profile
            if request.method == 'POST':
                data = request.data
                new_name = data.get('name')
                new_desc = data.get('desc')
                image = data.get('image')
                if user.nickname == new_name:
                    profile.description = new_desc
                    if image:
                        profile.image = write_img(image, user.nickname)
                    profile.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    exist = User.objects.filter(nickname=new_name)
                    user.nickname = new_name
                    if image:
                        user.image = write_img(image, user.nickname)
                    user.save()
                    profile.nickname = new_name
                    profile.description = new_desc
                    if image:
                        profile.image = write_img(image, user.nickname)
                    profile.save()
                    return Response(status=status.HTTP_200_OK)
    else:
        return Response({'msg': '你没有权限'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': '你必须先登录'}, status=status.HTTP_400_BAD_REQUEST)


# 返回文章
@api_view(['GET', 'POST'])
def article(request):
    the_topic = request.GET.get('topic')
    p = request.GET.get('p')
    user_id = request.GET.get('user_id')
    q = request.GET.get('q')
    if p:
        start = int(p)
        end = int(p) + 5
    else:
        start = 0
        end = 10
    if request.method == 'GET':
        if user_id:
            article_list = User.objects.get(id=user_id).article_author.all()
            serializer = ArticleSerializer(article_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif the_topic:
            article_list = Article.objects.filter(topics=the_topic)[:end]
            serializer = ArticleSerializer(article_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif q:  # 搜索
            article_list = Article.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q) | (Q(content__exact=q)))
            serializer = ArticleSerializer(article_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            article_list = Article.objects.all()[start:end]
            serializer = ArticleSerializer(article_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        article_topic = data.get('topic')

        article_description = data.get('description')
        article_content = data.get('content')
        article_title = data.get('title')
        user = request.user
        # if article_topic_id :
        #     if Topic.objects.filter(id=article_topic_id).exists():

        topic_exist = Topic.objects.filter(name=article_topic).exists()
        if topic_exist:
            article_topic = Topic.objects.filter(name=article_topic)[0]
        else:
            Topic.objects.create(name=article_topic)
            article_topic = Topic.objects.filter(name=article_topic)[0]
        print('topic:', article_topic.description)
        article_info = Article.objects.create(author=user, title=article_title, description=article_description,
                                              content=article_content,
                                              topics=article_topic)
        article_info.save()
        serializer = ArticleSerializer(article_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def article_detail(request, article_id):
    if request.method == 'GET':
        # 已登录用户判断是否对答案点赞
        if request.auth:
            user_id = request.user.id
            vote_exist = Vote.objects.filter(owner_id=user_id, give_to_id=article_id).exists()
            if vote_exist:
                vote_info = Vote.objects.get(owner_id=user_id, give_to_id=article_id).vote
            else:
                vote_info = 1
        else:
            vote_info = 1
        article_info = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article_info)

        data = {
            'article': serializer.data,
            'vote': vote_info
        }
        return Response(data, status=status.HTTP_200_OK)


# 具体那篇文章
@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def article_id(request, id):
    try:
        user = User.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        user = None
    if request.method == 'GET':
        p = request.GET.get('p')
        if p:
            end = int(p) + 5
        else:
            end = 5
        article_info = Article.objects.get(id=id)
        serializer = ArticleSerializer(article_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def comment(request):
    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        now_page = request.GET.get('page')
        comment_list_num = Comment.objects.all().filter(belong_to_id=article_id, parent=None).count()

        if int(comment_list_num) % 5 != 0:
            num_pages = int(int(comment_list_num) / 5 + 1)
        else:
            num_pages = int(int(comment_list_num) / 5)

        if not now_page:
            now_page = 1
            start = 0
        else:
            start = (int(now_page) - 1) * 5

        if comment_list_num <= start + 5:
            have_next = False
        else:
            have_next = True

        comment_list = Comment.objects.all().filter(belong_to_id=article_id, parent=None).order_by('-id')[
                       start:start + 5]
        page_list = get_page_list(current_page=int(now_page), left=3, right=4, page_number=num_pages)
        serializer = CommentSerializer(comment_list, many=True)
        data = {
            'data': serializer.data,
            'page_list': page_list,
            'now_page': now_page,
            'have_next': have_next
        }
        return Response(data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        parent_id = data.get('parent_id')
        content = data.get('content')
        reply_id = data.get('reply_id')
        article_id = data.get('article_id')
        article_info = Article.objects.get(id=article_id)
        user = request.user

        new_comment = Comment.objects.create(comment_user=user, belong_to_id=article_id,
                                             content=content, parent_id=parent_id, reply_to_id=reply_id)
        new_comment.save()

        comment_counts = Comment.objects.filter(belong_to_id=article_id).count()
        article_info.comment_counts = comment_counts
        article_info.save()

        return Response({'comment_counts': comment_counts}, status=status.HTTP_200_OK)


# 返回子评论
@api_view(['GET'])
def child_comments(request, comment_id):
    if request.method == 'GET':
        comment_info = Comment.objects.get(id=comment_id)
        child_comments_list = comment_info.child_comments
        serializer = ChildCommentSerializer(child_comments_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 返回对应的主题
@api_view(['GET'])
def topic(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'topic':
            q = request.GET.get('q')
            topic_list = Topic.objects.filter(Q(name__icontains=q))
        else:
            topic_list = Topic.objects.all()
        serializer = TopicSerializer(topic_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 用户投票
@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def user_vote(request):
    if request.method == 'POST':

        data = request.data
        vote = int(data['vote'])
        user_id = request.user.id
        article_id = data['article_id']
        article_info = Article.objects.get(id=article_id)
        exists = Vote.objects.filter(owner_id=user_id, give_to_id=article_id).exists()
        if exists:
            vote_info = Vote.objects.get(owner_id=user_id, give_to_id=article_id)
            # 如果已经点赞或反对，再次点击则取消
            if vote == vote_info.vote:

                Vote.delete(vote_info)
                if vote == 2:
                    article_info.like_counts -= 1
                if vote == 3:
                    article_info.dislike_counts -= 1
                article_info.save()

            # 把赞同改为反对或相反
            else:
                vote_info.vote = vote
                vote_info.save()
                if vote == 2:
                    article_info.like_counts += 1
                    article_info.dislike_counts -= 1
                if vote == 3:
                    article_info.like_counts -= 1
                    article_info.dislike_counts += 1
                article_info.save()
        else:
            Vote.objects.create(owner_id=user_id, give_to_id=article_id, vote=vote)
            if vote == 2:
                article_info.like_counts += 1
            if vote == 3:
                article_info.dislike_counts += 1
            article_info.save()

        # 把赞同反对数保存到数据库，测试发现这种用时间多一点
        # vote_like_count = Vote.objects.filter(give_to_id=answer_id, vote=2).count()
        # vote_dislike_count = Vote.objects.filter(give_to_id=answer_id, vote=3).count()
        # answer_info = Answer.objects.get(id=answer_id)
        # answer_info.like_counts = vote_like_count
        # answer_info.dislike_counts = vote_dislike_count
        # answer_info.save()
        return Response(status=status.HTTP_200_OK)


'''多少人喜欢用户的文章'''


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def user_article_like(request):
    user_id = request.user.id
    article_list = Article.objects.filter(vote__owner_id=user_id, vote__vote=2).all()
    serializer = ArticleSerializer(article_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


'''用户文章'''


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def user_article(request):
    user_id = request.user.id
    article_list = Article.objects.filter(author_id=user_id).all()
    serializer = ArticleSerializer(article_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


'''搜索文章'''


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def search(request):
    search_type = request.GET.get('type')
    q = request.GET.get('q')

    if search_type == 'content':
        article_list = Article.objects.filter(Q(title__icontains=q) |
                                              Q(description__icontains=q) |
                                              Q(content__icontains=q))
        serializer = ArticleSerializer(article_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif search_type == 'topic':
        topic = Topic.objects.filter(name__icontains=q)
        serializer = TopicSerializer(topic, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # article_list = Article.objects.filter(topics__name__icontains=q)
        # serializer = ArticleSerializer(article_list,many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    elif search_type == 'people':
        users = User.objects.filter(nickname__icontains=q)
        serializer = UserPartSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def getComment(request, user_id):
    # user = User.objects.get(id=user_id)
    # user_comment = user.comment_author.all().order_by('create_time')
    # serializer = CommentSerializer(user_comment, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    if request.user.id is not None:
        if int(request.user.id) == int(user_id):
            user = User.objects.get(id=user_id)
            user_comment = user.comment_author.all()
            serializer = CommentSerializer(user_comment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': '你没有权限'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg': '你必须先登录'}, status=status.HTTP_400_BAD_REQUEST)


# 输入图片
def write_img(image, username):
    if ('data:image/jpeg;base64,' in image):
        image = image.replace('data:image/jpeg;base64,', '')
    elif ('data:image/jpg;base64,' in image):
        image = image.replace('data:image/jpg;base64,', '')
    elif ('data:image/png;base64,' in image):
        image = image.replace('data:image/png;base64,', '')
    imgdata = base64.b64decode(image)
    # imgLocal = 'media/image/headportrait/'+username+'.png'
    imgLocal = 'image/headportrait/' + username + '.png'
    fp = open('media/' + imgLocal, 'wb')
    fp.write(imgdata)
    fp.close()
    return imgLocal
