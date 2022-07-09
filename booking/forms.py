from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField
from .models import Booking, TeachingDetail
BOOKING_TYPES = (
    ("TEACHING", "Teaching"),
    ("PERFORMANCE", "Performance"),
    ("EQUIPMENT", "Equipment hire"),
    ("PERFORMANCE AND EQUIPMENT", "Performance and Equipment hire"),
)

DAY_OF_WEEK = (
    ("MONDAY", "Monday"),
    ("TUESDAY", "Tuesday"),
    ("WEDNESDAY", "Wednesday"),
    ("THURSDAY", "Thursday"),
    ("FRIDAY", "Friday"),
    ("SATURDAY", "Saturday"),
    ("SUNDAY", "Sunday"),
)

INSTRUMENTS = (
    ("DRUM KIT", "Drum Kit"),
    ("PERCUSSION", "Percussion"),
    ("DULCIMER", "Dulcimer"),
    ("BODHRAN", "Dulcimer"),
    ("OTHER", "Other"),
)

PERFORMANCE_TYPES = (("REHEARSAL", "Rehearsal"), ("PERFORMANCE", "Performance"))

BUDGET_BANDS = (
    ("100-200", "100-200"),
    ("200-300", "200-300"),
    ("300-400", "300-400"),
    ("400-500", "400-500"),
    ("500+", "500+"),
)

class BookingForm(forms.Form):
    """
    Starting form will be the only visible form on page load.
    After user has selected a service the relevant form will be shown
    """
    class Meta:
        model = Booking

    # Starting form
    name = forms.CharField(label="Full name", max_length=50)
    email = forms.EmailField(max_length=254)
    service = forms.ChoiceField(choices=BOOKING_TYPES)

    # Teaching form
    postcode = forms.CharField(required=False)
    day = forms.ChoiceField(choices=DAY_OF_WEEK, required=False)
    time = forms.TimeField(required=False)
    instrument = forms.ChoiceField(choices=INSTRUMENTS, required=False)
    teaching_description = forms.CharField(max_length=254, required=False)

    # Performance Form
    date = forms.DateField(required=False)
    start_time = forms.TimeField(required=False)
    finish_time = forms.TimeField(required=False)
    performance_venue_postcode = forms.CharField(required=False)
    budget = forms.ChoiceField(choices=BUDGET_BANDS, required=False)
    performance_description = forms.CharField(max_length=254, required=False)

    # Equipment Form
    venue_postcode = forms.CharField(required=False)
    hiring_dates = SplitArrayField(forms.DateField(required=False), size=2, required=False)
    equipment_hired = SimpleArrayField(forms.CharField(), required=False)
    equipment_description = forms.CharField(
        max_length=254,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """
        Wraps fields into their relevant forms in order to manage multiple form logic
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div("name", "email", "service", css_class="starting-form"),
            Div(
                "postcode",
                "day",
                Field("time", css_class='teaching-picker'),
                "instrument",
                "teaching_description",
                css_class="teaching-form",
            ),
            Div(
                Field("date", css_class='date-picker'),
                Field("start_time", css_class='time-picker'),
                Field("finish_time", css_class='time-picker'),
                "performance_venue_postcode",
                "budget",
                "performance_description",
                css_class="performance-form",
            ),
            Div(
                "venue_postcode",
                Field("hiring_dates", css_class='equipment-picker'),
                "equipment_hired",
                "equipment_description",
                css_class="equipment-form",
            ),
            FormActions(
                Button("back", "Back", css_class='secondary-btn'),
                HTML(""" <p class='booking-steps-text'>Step 1 of 2 </p>"""),
                Button("next", "Next"),
                Submit("submit", "submit"),
                css_class="booking-steps",
            ),
        )

class UpdateTeachingForm(forms.ModelForm):
    """
    Form to be used for updating a teaching Booking
    """
    class Meta: # pylint: disable=missing-class-docstring
        model = TeachingDetail
        exclude = ['booking', 'Address']
    
    def __init__(self, *args, **kwargs):
        """
        Wraps fields into their relevant forms in order to manage multiple form logic
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button("cancel", "cancel", css_class='secondary-btn'),)
        self.helper.add_input(Submit('submit', 'submit',))
