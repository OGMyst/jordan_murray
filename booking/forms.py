from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

BOOKING_TYPES =(
    ('TEACHING', 'Teaching'),
    ('PERFORMANCE', 'Performance'),
    ('EQUIPMENT', 'Equipment hire'),
    ('PERFORMANCE AND EQUIPMENT', 'Performance and Equipment hire'),
)

DAY_OF_WEEK=(
    ('MONDAY', 'Monday'),
    ('TUESDAY', 'Tuesday'),
    ('WEDNESDAY', 'Wednesday'),
    ('THURSDAY', 'Thursday'),
    ('FRIDAY', 'Friday'),
    ('SATURDAY', 'Saturday'),
    ('SUNDAY', 'Sunday'),
)

INSTRUMENTS=(
    ('DRUM KIT', 'Drum Kit'),
    ('PERCUSSION', 'Percussion'),
    ('DULCIMER', 'Dulcimer'),
    ('BODHRAN', 'Dulcimer'),
    ('OTHER', 'Other')
)

PERFORMANCE_TYPES =(
    ('REHEARSAL', 'Rehearsal'),
    ('PERFORMANCE', 'Performance')
)

BUDGET_BANDS = (
    ('100-200', '100-200'),
    ('200-300', '200-300'),
    ('300-400', '300-400'),
    ('400-500', '400-500'),
    ('500+', '500+'),

)
class BookingForm(forms.Form):
    """
    Step one of booking form. Step two corresponds to the service picked.
    """
    name = forms.CharField(label='Full name', max_length=50)
    email = forms.EmailField(max_length=254)
    service = forms.ChoiceField(choices=BOOKING_TYPES)

class TeachingForm(forms.Form):
    """
    Step two of form
    """
    postcode = forms.CharField()
    day = forms.ChoiceField(choices=DAY_OF_WEEK)
    time = forms.TimeField(required=False)
    instrument = forms.ChoiceField(choices=INSTRUMENTS)
    description = forms.CharField(max_length=254, required=False)

    def __init__(self, *args, **kwargs):
        """
        Add classes to form
        """
        super().__init__(*args, **kwargs)

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'hidden'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    'postcode',
                    'day',
                    'time',
                    'instrument',
                    'description',
                    css_class = 'hidden'
                )
            )
        )

class PerformanceForm(forms.Form):
    """
    Step two of form
    """
    date_and_time = forms.DateTimeField()
    performance_venue_postcode = forms.CharField()
    budget = forms.ChoiceField(choices=BUDGET_BANDS)
    description = forms.CharField(max_length=254, required=False)

class EquipmentForm(forms.Form):
    """
    Step two of form
    """
    date_and_time = forms.DateTimeField()
    performance_venue_postcode = forms.CharField()
    budget = forms.ChoiceField(choices=BUDGET_BANDS)
    description = forms.CharField(max_length=254, required=False)
