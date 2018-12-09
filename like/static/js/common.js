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

    $('.ui.sticky').sticky({
        context: "#lg-content"
    });

    var url = "/api/v1/post";
    var page = 2;
    function loadPost(page=page) {
        $.ajax({
                url: url,
                type: "GET",
                data: {
                    page: page
                },
                success: function (data) {
                    $("#lg-content").append(data);
                    flask_moment_render_all();
                    $('.ui.sticky').sticky({
                        context: "#lg-content"
                    });
                    page += 1;
                },
            });
    }

    loadPost(1);


    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() === $(document).height()) {
            loadPost(page);
        }
    });
});

