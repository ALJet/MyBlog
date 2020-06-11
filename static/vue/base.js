// 回到顶部
$(function () {
    $('#back-to-top').on('click', function () {
        $('html').animate({
            scrollTop: 0
        }, 1000);
    });

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > $(window).height()) {
            $('#back-to-top').fadeOut();
        } else {
            $('#back-to-top').fadeIn();
        }
    });
});

