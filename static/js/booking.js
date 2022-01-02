let selectedService = $('#id_service').val().toLowerCase()

// Selected service determines which fields should be shown for the second step
$('#id_service').change(function(){
    selectedService = $('#id_service').val().toLowerCase()

})

// Using selected service, when the user selects the next button the second step of the form is shown
$('#button-id-step-one').click(function(){
    $('.starting-form').hide()
    $(`.${selectedService}-form`).show() // Second step of the form
})