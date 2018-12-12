$(document).ready(function () {
    $(".follow-user").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var statusE = self.children("span");
        var iconE = self.children("i");
        var aE = $(".statistics a:nth-child(2)");
        var followerCount = Number(aE.find(".value").text());

        iconE.toggleClass("orange");
        if (statusE.text() === "关注") {
            statusE.text("取消关注");
            aE.find(".value").text(followerCount+1);
        } else {
            statusE.text("关注");
            aE.find(".value").text(followerCount-1);
        }


        $.ajax({
            url: "/user/follow",
            type: "GET",
            data: {
                id: self.data("id")
            },
            success: function (data) {

            }
        });
    });
});