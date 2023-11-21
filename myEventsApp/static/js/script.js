// add event listeners
$(document).ready(function () {
    let curr;
    // event listener for td cells in calendar
    $('table').on('click', 'td', function (event) {
        event.preventDefault();
        $('.events-display').empty()
        $(curr).css('background-color', 'revert');
        $(this).css('background-color', 'lightgrey');
        curr = this;
        $('.events-display').css('display', 'block');
    });

})

