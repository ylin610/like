$(document).ready(function () {
    // ----------Ajax初始化----------
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    // ----------moment----------
    moment.locale("zh-cn");

    function flask_moment_render(elem) {
        $(elem).text(eval('moment("' + $(elem).data('timestamp') + '").' + $(elem).data('format') + ';'));
        $(elem).removeClass('flask-moment').show();
    }

    function flask_moment_render_all() {
        $('.flask-moment').each(function () {
            flask_moment_render(this);
            if ($(this).data('refresh')) {
                (function (elem, interval) {
                    setInterval(function () {
                        flask_moment_render(elem)
                    }, interval);
                })(this, $(this).data('refresh'));
            }
        })
    }

    // ----------粘性侧边栏----------
    function stick() {
        $('.ui.sticky').sticky({
            context: '#lg-content'
        });
    }

    // ----------绑定点赞、收藏按钮的点击事件----------
    function act() {
        var self = $(this);
        let urlMap = {
            likeComment: "/user/action/comment/like",
            likePost: "/user/action/post/like",
            collectPost: "/user/action/post/collect",
            likeTopic: "/user/action/topic/like",
            likeUser: "/user/action/user/like"
        };
        var action = self.data("action");
        var url = urlMap[action];

        function shift(elem) {
            var iconE = elem.children("i");
            var countE = elem.children("span");
            var num = Number(countE.text());
            if (iconE.hasClass("orange")) {
                countE.text(num - 1);
            } else {
                countE.text(num + 1);
            }
            iconE.toggleClass("orange");
        }
        if (action === "likeComment") {
            $("span[data-id='" + self.data("id") + "']").each(function () {
                shift($(this));
            });
        } else {
            shift($(this));
        }

        $.ajax({
            url: url,
            type: "GET",
            data: {
                id: self.data("id")
            },
            success: function (data) {
            }
        });
    }

    function bindAction() {
        $(".to-bind").each(function () {
            this.onclick = act;
            $(this).removeClass("to-bind");
        });
    }

    // ----------回复评论----------
    function reply() {
        var self = $(this);
        let content = self.prev().val();
        let commentId = self.data("commentid");
        console.log(content);

        $.ajax({
            type: "GET",
            url: "/user/reply",
            data: {
                comment_id: commentId,
                content: content
            },
            success: function (data) {
                if (data["code"] === 200) {
                    window.location.reload();
                }
            }
        });
    }

    function bindReply() {
        $(".to-bind-reply").each(function () {
            this.onclick = reply;
            $(this).removeClass("to-bind-reply");
        });
    }

    function showReplyInput() {
        var self = $(this);
        var actionsE = self.parent();
        var commentId = self.data("replyto");

        if (actionsE.hasClass("reply-active")) {
            var replyE = actionsE.next();
            replyE.remove();
        } else {
            $.ajax({
                type: "GET",
                url: "/api/v1/reply_input",
                data: {
                    comment_id: commentId
                },
                success: function (data) {
                    if (data["code"] === 200) {
                        actionsE.after(data["data"]);
                        bindReply();
                    }
                }
            });
        }
        actionsE.toggleClass("reply-active");
    }

    function bindShowReplyInput() {
        $(".to-bind-replyInput").each(function () {
            this.onclick = showReplyInput;
            $(this).removeClass("to-bind-replyInput");
        });
    }

    // ----------瀑布流----------
    var urlMap = {
        post: "/api/v1/post",
        comment: "/api/v1/comment",
        discovery: "/api/v1/discovery",
        collection: "/api/v1/collection"
    };
    var next_page = 1;
    var hasNext = true;

    function loadPost(page) {
        $.ajax({
            url: urlMap[stream_type],
            type: "GET",
            data: {
                page: page,
                topic_id: topic_id,
                post_id: post_id,
                user_id: user_id
            },
            success: function (res) {
                $("#stream").append(res["data"]["html"]);
                flask_moment_render_all();
                bindAction();
                bindShowReplyInput();
                stick();
                next_page += 1;
                hasNext = res["data"]["has_next"];
            },
        });
    }

    loadPost(next_page);

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() === $(document).height()) {
            if (hasNext) {
                loadPost(next_page);
            }
        }
    });
});

