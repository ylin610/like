$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $('.ui.sticky')
        .sticky({
            context: '#lg-content'
        })
    ;

    var url = '/api/v1/post';
    var page = 2;
    var loadPost = function (page=page) {
        $.ajax({
                url: url,
                type: 'GET',
                data: {
                    page: page
                },
                success: function (data) {
                    $("#lg-content").append(data);
                    page += 1;
                },
                error: function (e) {
                }
            });
    };
    loadPost(1);

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() === $(document).height()) {
            loadPost(page);
        }
    });
});

