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


