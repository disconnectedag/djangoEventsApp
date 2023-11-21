// event handler for a user clicking attend on an event
$(document).ready(function () {
    $('#comment-form').on("submit", function (e) {
        let event_id = $(this).attr('data-event-id');
        let ajax_url = $(this).attr('data-ajax-url');
        let body = $('#body').val()
        e.preventDefault()
        $.ajax({
            url: ajax_url,
            data: {
                event_id: event_id,
                body: body
            },
            type: "POST",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken}
        })
            .done(function (json) {
                if (json.success === 'success') {
                    if ($('.comments-container').text().trim() === 'No comments yet.') {
                        $('.comments-container').empty();
                    }
                    let formattedTime = naturalTime(json.time)
                    let baseUrl = $('.comments-section').data('profile-url');
                    let profileUrl = baseUrl.replace('USERNAME', json.name);
                    let newComment = `<div class="comment">
                    <p><strong><a href="${profileUrl}">${json.name}</a>:</strong> ${json.body}</p>
                    <p>Posted ${formattedTime}</p></div>`;
                    $('.comments-container').prepend(newComment);
                    $('#body').val('')
                    location.reload()
                }
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                // console.log("Status: " + status);
                // console.dir(xhr);
            })

    })

    $('.delete-comment').on('click', function () {
        let comment_id = $(this).attr('data-comment-id')
        let ajax_url = $(this).attr('data-ajax-url');
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_id: comment_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (json) {
                $('#comment-' + comment_id).remove();
            })
    })
    $('#attend-btn').click(function () {
        let event_id = $(this).attr('data-event-id');
        let ajax_url = $(this).attr('data-ajax-url');
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                event_id: event_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    let countElement = $('#attendees-counter');
                    let newCount = json.attendCount;
                    $(countElement).text(newCount);
                    $('#attend-btn').attr('disabled', true).css("background-color", 'lightgrey')
                } else {
                    alert("Error" + json.error);
                }

            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                // console.log("Status: " + status);
                // console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
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

function naturalTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.round((now - date) / 1000);
    const minutes = Math.round(seconds / 60);
    const hours = Math.round(minutes / 60);
    const days = Math.round(hours / 24);

    if (seconds < 45) return 'a few seconds ago';
    if (seconds < 90) return 'a minute ago';
    if (minutes < 45) return minutes + ' minutes ago';
    if (minutes < 90) return 'an hour ago';
    if (hours < 24) return hours + ' hours ago';
    if (hours < 48) return 'yesterday';
    if (days < 30) return days + ' days ago';
    if (days < 60) return 'a month ago';
    if (days < 365) return Math.round(days / 30) + ' months ago';
    return Math.round(days / 365) + ' years ago';
}

const csrftoken = getCookie('csrftoken');
