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

    // ----------动态点赞和收藏----------
    $(".like-post").click(function (event) {
        event.preventDefault();
        var action = "like";
        actPost(action, $(this));
    });
    $(".collect-post").click(function (event) {
        event.preventDefault();
        var action = "collect";
        actPost(action, $(this));
    });

    function actPost(action, elem) {
        var countE = elem.children("span");
        var iconE = elem.children("i");
        var num = Number(countE.text());
        if (iconE.hasClass("orange")) {
            countE.text(num - 1);
        } else {
            countE.text(num + 1);
        }
        iconE.toggleClass("orange");

        $.ajax({
            url: "/post/" + action,
            type: "GET",
            data: {
                post_id: elem.data("id")
            },
            success: function (data) {
                console.log(data);
            }
        });
    }

    // ----------评论点赞----------
    function likeComment() {
        event.preventDefault();
        var self = $(this);
        var commentId = self.parent().parent().parent().data("id");

        function shiftStatus(elem) {
            var countE = elem.children("span");
            var iconE = elem.children("i");
            var num = Number(countE.text());
            if (iconE.hasClass("orange")) {
                countE.text(num - 1);
            } else {
                countE.text(num + 1);
            }
            iconE.toggleClass("orange");
        }

        $("div[data-id='" + commentId + "']").each(function () {
            shiftStatus($(this).find("span.like-comment"));
        });

        $.ajax({
            url: "/comment/like",
            type: "GET",
            data: {
                comment_id: commentId
            },
            success: function (data) {
                console.log(data);
                switch (data["code"]) {
                    case 401:
                        window.location = "/login";
                        break;
                    case 200:
                        break;
                    case 400:
                        break;
                }
            }
        });
    }

    function bind() {
        $(".to-bind").each(function () {
            this.onclick = likeComment;
            $(this).removeClass("to-bind");
        });
    }

    // ----------瀑布流----------
    var url = {
        post: "/api/v1/post",
        comment: "/api/v1/comment",
    };
    var next_page = 1;
    var hasNext = true;

    function loadPost(page) {
        $.ajax({
            url: url[content_type],
            type: "GET",
            data: {
                page: page,
                topic: topic,
                post_id: post_id
            },
            success: function (res) {
                $("#stream").append(res["data"]["html"]);
                flask_moment_render_all();
                bind();
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

