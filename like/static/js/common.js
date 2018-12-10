$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

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

    function stick() {

    }

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
                success: function (data) {
                    $("#stream").append(data['html']);
                    flask_moment_render_all();
                    stick();
                    next_page += 1;
                    hasNext = data['has_next'];
                },
            });
    }

    loadPost(next_page);


    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() === $(document).height()) {
            if(hasNext) {
                loadPost(next_page);
            }
        }
    });
});

