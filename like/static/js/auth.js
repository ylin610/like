$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("#get-captcha").click(function (event) {
        event.preventDefault();
        var self = $(this);
        email = $("#email").val();
        $.ajax({
            url: '/email_captcha',
            type: "GET",
            data: {
                email: email
            },
            success: function (data) {
            }
        });
        self.toggleClass('disabled');
        var time = 60;
        var timer = setInterval(function () {
            time--;
            self.text(time + "秒后再次发送");
            if (time <= 0) {
                self.toggleClass('disabled');
                clearInterval(timer);
                self.text("再次发送");
            }
        }, 1000);
    });
});