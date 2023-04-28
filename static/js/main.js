
$(document).ready(function () {
    $('#avatar').click(function () {
        $('#profile-menu').toggleClass('hidden grid');
    });

    $('.message').fadeOut(5000, "swing");

    $('#profile-menu').focusout(function () {
        $('#profile-menu').addClass('hidden');
        console.log("focusout");
    });

    // Workaround for Django MarkdownX
    $('#id_content')[0].cols = 60;
});