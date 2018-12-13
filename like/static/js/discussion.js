var messageE = $("#message-box");
function scrollToBottom() {
    messageE.scrollTop(messageE[0].scrollHeight);
}

$(document).ready(function () {
    flask_moment_render_all();
    scrollToBottom();

    var socket = io();
    console.log('sending join message');
    socket.emit('join', {
        disc_id: disc_id,
        user_id: user_id
    });

    $("#stat-btn").click(function () {
        var content = $(this).prev().val();

        console.log('sending new message');
        socket.emit("new message", {
            user_id: user_id,
            disc_id: disc_id,
            content: content
        });
    });

    socket.on("new message", function (data) {
        console.log('recv new message');
        messageE.append(data["html"]);
        scrollToBottom();
    });
});