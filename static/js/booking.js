let selectedService = $('#id_service').val().toLowerCase()

let formType = {
    'teaching': 'teaching-picker',
    'performance': 'performance-picker',
    'equipment': 'equipment-picker',

}

// Selected service determines which fields should be shown for the second step
$('#id_service').change(function(){
    selectedService = $('#id_service').val().toLowerCase()

})

// Using selected service, when the user selects the next button the second step of the form is shown
$('#button-id-step-one').click(function(){
    $('.starting-form').hide()
    $(`.${selectedService}-form`).show() // Second step of the form
    
    materializeDatetimePicker() //Forms have different date/time/datetime input requirements
})

function materializeDatetimePicker(){
    switch (selectedService){
        case 'teaching':
            $(`.${formType[selectedService]}`).timepicker();
            break;
        case 'performance':
            $('.time-picker').timepicker();
            $('.date-picker').datepicker();          
            makeTimeValid();
            break;
        case 'equipment':
            $(`.${formType[selectedService]}`).datepicker();
        }
}

function makeTimeValid(){
    $('#submit-id-submit').click(function(event){
        $('.time-picker').each(function(){
            this.value = this.value.replace(/(am|pm)/i, '').trim()            
        })
    });
}