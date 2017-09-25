$(document).ready(function () {
    $("#about-btn").click(function (event) {
        alert("You clicked the button using JQuery!");
    });

    $("p").hover(function () {
        $(this).css('color', 'red');
    }, function () {
        $(this).css('color', 'blue');
    });

    $("#about-btn").click(function (event) {
        msgstr = $("#msg").html();
        msgstr = msgstr + "ooo";
        $("#msg").html(msgstr)
    });

    $(".ouch").click(function (event) {
        alert("You clicked me! ouch!");
    });

    $(".ouch").addClass('btn btn-primary');

    $("#likes").click(function () {
        alert("click me!");
        var catid;
        catid = $(this).attr("data-catid");
        $.get("/rango/like/", {category_id: catid}, function (data) {
            $("#like_count").html(data);
            $("#likes").hide();
        });
    });

});


