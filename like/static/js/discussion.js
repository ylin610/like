var messageE = $("#message-box");
function scrollToBottom() {
    messageE.scrollTop(messageE[0].scrollHeight);
}

$(document).ready(function () {
    flask_moment_render_all();
    scrollToBottom();

    $("#join-discussion").click(function () {
        $.ajax({
            type: "GET",
            url: "/discussion/join",
            data: {
                disc_id: disc_id
            },
            success: function (data) {
                if (data["code"] == 200) {
                    window.location.reload();
                }
            }
        });
    });

    var socket = io();
    socket.emit('join', {
        disc_id: disc_id
    });

    $("#stat-btn").click(function () {
        var inputE = $(this).prev();
        var content = inputE.val();
        inputE.val("");

        socket.emit("new message", {
            disc_id: disc_id,
            content: content
        });
    });

    socket.on("new message", function (data) {
        if (data["html"]) {
            messageE.append(data["html"]);
            scrollToBottom();
        }
    });
});