from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField
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
    # Starting form
    name = forms.CharField(label="Full name", max_length=50)
    email = forms.EmailField(max_length=254)
    service = forms.ChoiceField(choices=BOOKING_TYPES)

    # Teaching form
    postcode = forms.CharField()
    day = forms.ChoiceField(choices=DAY_OF_WEEK)
    time = forms.TimeField(required=False)
    instrument = forms.ChoiceField(choices=INSTRUMENTS)
    teaching_description = forms.CharField(max_length=254, required=False)

    # Performance Form
    date_and_time = forms.DateTimeField()
    performance_venue_postcode = forms.CharField()
    budget = forms.ChoiceField(choices=BUDGET_BANDS)
    performance_description = forms.CharField(max_length=254, required=False)

    # Equipment Form
    venue_postcode = forms.CharField()
    hiring_dates = SplitArrayField(forms.DateField(), size=2)
    equipment_hired = SimpleArrayField(forms.CharField())
    equipment_description = forms.CharField(max_length=254, required=False)

    def __init__(self, *args, **kwargs):
        """
        Add classes to form
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper[0:3].wrap_together(Div, css_class="starting-form")
        self.helper[1:6].wrap_together(Div, css_class="teaching-form")
        self.helper[2:6].wrap_together(Div, css_class="performance-form")
        self.helper[3:7].wrap_together(Div, css_class="equipment-form")
