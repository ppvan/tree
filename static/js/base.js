console.log("base.js loaded");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// const csrftoken = getCookie('csrftoken');
window.$ = jQuery;
$(document).ready(function () {
    // UI Effects section
    $('#avatar').click(function () {
        $('#profile-menu').toggleClass('hidden grid');
    });

    $('.message').fadeOut(5000, "swing");

    $('#profile-menu').focusout(function () {
        $('#profile-menu').addClass('hidden');
        console.log("focusout");
    });

    $('#quantity-decrease').click(function () {
        let quantity = parseInt($('#id_quantity').val());
        if (quantity > 1) {
            $('#id_quantity').val(quantity - 1);
        }
    });

    $('#quantity-increase').click(function () {
        let quantity = parseInt($('#id_quantity').val());
        $('#id_quantity').val(quantity + 1);
    });

    // Workaround for Django MarkdownX
    var contentElem = $("#id_content");
    if (contentElem.length) {
        contentElem.prop("cols", 60); // Set the cols property to 40
    }

    // End of UI Effects section
});