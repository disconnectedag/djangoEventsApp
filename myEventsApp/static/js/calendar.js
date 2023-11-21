// event handler for a user clicking attend on an event
$(document).ready(function () {
    $('.calendar td').click(function() {
        let date = parseInt($(this).closest('td').text());
        let tableElem = $(this).closest('table')
        let ajax_url = tableElem.attr('data-ajax-url');
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                event_day: date
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
                if(json.success == 'success') {
                    let eventList = JSON.parse(json.filtered_events)
                    console.log(eventList)
                    $('.events-display').append(`<h3 class="title-side-events">Events on the ${date}th</h3>`)
                    for(let event in eventList) {
                        $('.events-display').append(`<div class="event">${eventList[event].fields.title}</div>`)
                    }

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
const csrftoken = getCookie('csrftoken');
