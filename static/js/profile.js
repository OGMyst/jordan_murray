let calendarTitles = $('.calendar-card h4')
let curr = ''
let prev = ''

// Removes duplicate dates from the calendar items
calendarTitles.each(function(index){
    curr = $(this).text()
    isMatch = Boolean(curr === prev)
    if(isMatch){
        $(this).hide()
    }else{
        prev = $(this).text()
    }
})