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

    // Workaround for Django MarkdownX
    var contentElem = $("#id_content");
    if (contentElem.length) {
        contentElem.prop("cols", 60); // Set the cols property to 40
    }

    // End of UI Effects section
});

function callSearchAPI(query, callback) {
    if (query.length > 0) {
        console.log(query);
        $.ajax({
            url: "/api/search/",
            type: "GET",
            data: {
                "q": query
            },
            success: function (data) {
                callback(data);
            },
            error: function (error) {
                console.log(error);
                callback([]);
            }
        });
    } else {
        console.log("Empty query");
        callback([]);
    }
}

function updateResult(data) {
    let searchResult = $("#search-result");
    searchResult.removeClass("hidden");
    searchResult.empty();
    searchResult.html(data);
}

let timerId = undefined;
let debounceFunction = function (func, delay) {
    // Cancels the setTimeout method execution
    clearTimeout(timerId)

    // Executes the func after delay time.
    timerId = setTimeout(func, delay)
}

$("#search-form>input").on("input", function () {

    let query = $(this).val();

    debounceFunction(function () {
        callSearchAPI(query, updateResult)
    }, 50);
});