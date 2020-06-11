from django.db.models import Q
from django.shortcuts import render
from .models import Article, Topic, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def Index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, "blog/index.html", context)


def topic_page(request):
    topic_name = request.GET.get('t')
    context = {'topic_name': topic_name}
    return render(request, "blog/topic.html", context)


def topic_detail_page(request, topic_id):
    topic_name = Article.objects.filter(topics=topic_id)

    context = {'topic_name': topic_name}

    return render(request, "blog/topic.html", context)


def search(request):
    q = request.GET.get('q')
    if q:
        article_list = Article.objects.filter(Q(title__icontains=q) |
                                              Q(content__icontains=q))
    else:
        q = None
        article_list = None
    context = {
        'q': q,
        'article_list': article_list,
    }
    return render(request, 'search.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article_id': article_id,
               'article': article}
    return render(request, "blog/article_detail.html", context)


def user_articles(request, user_id):
    user_info = User.objects.get(id=user_id)
    context = {
        'user_id': user_id,
        'user_info': user_info
    }

    return render(request, "blog/user_articles.html", context)


def edit_user(request, user_id):
    context = {
        'user_id': user_id,
    }
    return render(request, 'blog/edit_user.html', context)


def add_article(request):
    return render(request, 'blog/add_my_article.html')


def user_personal(request, user_id):
    # context = {'user_id': user_id}
    # return render(request, "blog/user_personal.html", context)
    print('user_id', user_id)
    print('request.user.id', request.user)
    if int(request.user.id) == int(user_id):
        context = {'user_id': user_id}
        return render(request, "blog/user_personal.html", context)
    else:
        context = {'user_id': user_id}
        return render(request, 'blog/index.html', context)


def user_comment(request, user_id):
    context = {'user_id': user_id}
    return render(request, "blog/user_comment.html", context)


def test(request):
    context = {'test': test}
    return render(request, "blog/test.html", context)
