$(document).ready(function () {
    $('#edit-form').on('submit', function (e) {
        e.preventDefault()
        let comment_body = $('#comment-text').val()
        let ajax_url = $(this).attr('data-ajax-url');
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_body: comment_body
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (json) {
                window.location.href = json.redirect_url;
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                // console.log("Status: " + status);
                // console.dir(xhr);
            })
    })
})

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

const csrftoken = getCookie('csrftoken');