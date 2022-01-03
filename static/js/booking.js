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
    $(`.${formType[selectedService]}`).datepicker();
}