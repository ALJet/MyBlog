$('#drop_down')
    .dropdown({
        on: 'hover'
    });


Vue.config.delimiters = ["[[", "]]"];
Vue.filter('timeDeal', function (create_time) {
    return create_time
});
vm_index = new Vue({
    el: '#app',
    data: {
        moreOrNot: '加载更多',
        articles: [],
        topics: [],
        comments: [],
        comment_input_show: true,
        comment_show: false,
        comment_content: '',
        login_or: false,
        user_info: '',
        vote_or: '',
        username: '',
        password: '',
        email: '',
        username_err: '',
        password_err: '',
        email_err: '',
        msgShow: false,
        page_lists: [],
        pre: true,
        havePre: false,
        haveNext: false,
        now_page: 1,
        nowPage: '',
        q: '',
        article_content: '',
        article: {
            title: '',
            desc: '',
            topic: ''
        },

    },
    methods: {
        // {#添加文章按钮 未登录弹出注册框#}
        addArticleBtn: function () {
            var self = this;
            if (self.user_info == '') {
                return $('#register-modal').modal('show')
            } else {
                return $('#article-modal').modal('show');
            }
        },
        // {# 添加文章 #}
        addArticle: function () {
            var self = this;
            reqwest({
                url: '/api/articles/',
                type: 'json',
                method: 'post',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                data: {
                    title: self.article.title,
                    desc: self.article.desc,
                    topic: self.article.topic
                },
                success: function (resp) {
                    window.location.href = '/articles/' + resp.id + '/'
                }
            })
        },
        ifLogin: function () {
            var self = this;
            if (self.user_info == '') {
                return $('#register-modal').modal('show')
            }
        },
        logIn: function () {
            var self = this;
            reqwest({
                url: '/api/login/',
                type: 'json',
                method: 'post',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                data: {
                    username: self.username,
                    password: md5(self.password)
                },
                success: function (resp) {
                    Cookies.set('token', resp.token)
                    location.reload()
                }
            })
        },
        logOut: function () {
            Cookies.remove('token');
            location.reload()
        },
        // {# 预先加载，用户判断用户身份 #}
        request_user: function () {
            var self = this;
            reqwest({
                url: '/api/users/now/',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    self.user_info = resp;
                    self.login_or = true
                },
                error: function (err) {
                    json_msg = JSON.parse(err.response);
                    self.login_or = false
                }
            })
        },
        displayBody: function () {
            document.querySelector('#home-page').style.cssText = "display:"
        },
        getArticle: function () {
            console.log(Cookies.get('token'))
            var self = this;
            reqwest({
                url: '/api/articles/',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    if (resp.length < 10) {
                        self.moreOrNot = '没有了'
                        return
                    }
                    // {# 为每个article添加默认不显示评论和不显示全部内容 #}
                    for (r in resp) {
                        resp[r].show_all_comments = false;
                        resp[r].show_all_content = false;
                        resp[r].like_or = 1;
                    }
                    self.articles = resp;
                }
            })
        },
        getComment: function (article, page) {
            var self = this;
            var articles = self.articles
            for (r in articles) {
                articles[r].show_all_comments = false;
            }
            reqwest({
                url: '/api/comments?page=' + page + '&article_id=' + article.id,
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    var comments = resp.data
                    for (c in comments) {
                        var comment = comments[c]
                        comment.comment_reply_input = false;
                        comment.comment_content = '';
                        for (d in comment.child_comments) {
                            comment.child_comments[d].comment_reply_input = false;
                            comment.child_comments[d].comment_content = ''
                        }
                    }
                    ;
                    article.article_comments = comments;
                    self.now_page = resp.now_page;
                    self.page_lists = resp.page_list;
                    article.show_all_comments = true;
                    self.haveNext = resp.have_next

                    if (page == 1) {
                        self.havePre = false
                    } else {
                        self.havePre = true
                    }
                }
            })
        },
        getChildComment: function (comment) {
            reqwest({
                url: '/api/child_comments/' + comment.id + '/',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    comment.child_comments = resp
                }
            })
        },
        getNextCom: function (article) {

            next_page = parseInt(this.now_page) + 1
            this.getComment(article, next_page)
        },
        getPreCom: function (article) {
            pre_page = parseInt(this.now_page) - 1
            this.getComment(article, pre_page)
        },
        loadMoreArticle: function () {
            var self = this;
            reqwest({
                url: '/api/articles?p=' + self.articles.length,
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    for (r in resp) {
                        resp[r].show_all_comments = false
                    }
                    // {# 加载之前的文章数量 #}
                    before_len = self.articles.length;
                    // {# 新加载的文章 push到列表中 #}
                    for (a in resp) {
                        for (c in self.articles)
                            if (c.id != a.id)
                                self.articles.push(resp[a])
                    }
                    // {# 加载之后的数量 #}
                    after_len = self.articles.length;
                    // {# 默认每次加载5个，如果少于5个，即没有了 #}
                    if (after_len - before_len < 5) {
                        self.moreOrNot = '没有了'
                    }
                }
            })
        },
        showAllContent: function (article) {
            var self = this;
            reqwest({
                url: '/api/articles/' + article.id,
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                success: function (resp) {
                    article.like_or = resp.vote;
                    article.like_counts = resp.article.like_counts;
                    article.show_all_content = true;
                    article.content = resp.article.content;
                }
            })
        },
        showAllCommentsSwitch: function (article) {
            article.show_all_comments = !article.show_all_comments;
        },
        commentReplyInput: function (comment) {
            comment.comment_reply_input = !comment.comment_reply_input
        },
        addComment: function (article) {
            var self = this;
            reqwest({
                url: '/api/comments/',
                method: 'post',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                data: {
                    content: self.comment_content,
                    article_id: article.id
                },
                success: function (resp) {
                    var comment_counts = resp.comment_counts;
                    page = Math.ceil(comment_counts / 5);
                    self.getComment(article, page);
                    self.comment_content = ''
                }
            })
        },
        replyComment: function (article, comment) {
            var self = this;
            reqwest({
                url: '/api/comments/',
                method: 'post',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                data: {
                    content: comment.comment_content,
                    article_id: article.id,
                    parent_id: comment.id,
                    reply_id: comment.id
                },
                success: function (resp) {
                    var comment_counts = resp.comment_counts;
                    page = Math.ceil(comment_counts / 5);
                    self.getComment(article, page);
                    comment.comment_content = ''
                }
            })
        },
        replyChildComment: function (article, comment, child_comment) {
            var self = this;
            reqwest({
                url: '/api/comments/',
                method: 'post',
                type: 'json',
                headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                data: {
                    content: child_comment.comment_content,
                    article_id: article.id,
                    parent_id: comment.id,
                    reply_id: child_comment.id
                },
                success: function (resp) {
                    var comment_counts = resp.comment_counts;
                    page = Math.ceil(comment_counts / 5);
                    self.getComment(article, page);
                    child_comment.comment_content = ''
                }
            })
        },
        userVote: function (vote, article) {
            var self = this;
            if (self.login_or == false) {
                return $('#register-modal').modal('show')
            } else {
                reqwest({
                    url: '/api/user_vote/',
                    type: 'json',
                    method: 'post',
                    headers: Cookies.get('token') ? {'Authorization': 'Token ' + Cookies.get('token')} : {},
                    data: {
                        vote: vote,
                        article_id: article.id
                    },
                    success: function () {
                        self.showAllContent(article)
                    }
                })
            }
        },
        registerUser: function () {
            var self = this;
            reqwest({
                url: '/api/register/',
                method: 'post',
                type: 'json',
                data: {
                    nickname: this.username,
                    password: this.password,
                    email: this.email,
                },
                success: function (resp) {
                }
            })

        }

    },
    ready: function () {
        this.request_user();
        this.getArticle();
        this.displayBody();
    }
})