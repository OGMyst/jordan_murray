// Removes duplicate dates from the calendar items
function removeDuplicateDates() {
    let calendarTitles = $('.calendar-card h4')
    let curr = ''
    let prev = ''

    calendarTitles.each(function (index) {
        curr = $(this).text()
        isMatch = Boolean(curr === prev)
        if (isMatch) {
            $(this).hide()
        } else {
            prev = $(this).text()
        }
    })
}

//Adds dropdowns to rehearsal and concert times on cards
function addDropdowns() {

    options = {
        'hover': true,
        'coverTrigger': false,
        'constrainWidth':false,
        'alignment': 'right',
    }

    rehearsalDropdowns = M.Dropdown.init($('.dropdown-trigger'), options);

    //Materliaze automatically adds btn class. Don't want dropdown to use those class attributes 
    $(rehearsalDropdowns).each((index, value) => {
        $(value.el).removeClass('btn')
    })
}

removeDuplicateDates();
addDropdowns();

