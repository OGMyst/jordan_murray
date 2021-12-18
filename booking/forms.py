from django import forms

BOOKING_TYPES =(
    ('TEACHING', 'Teaching'),
    ('PERFORMANCE', 'Performance'),
    ('EQUIPMENT', 'Equipment hire'),
    ('TEACHING AND EQUIPMENT', 'Teaching and Equipment hire'),
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
class BookingForm(forms.Form):
    """
    Step one of booking form. Service selected corresponds to a separate step two.
    """
    name = forms.CharField(label='Full name', max_length=50)
    email = forms.EmailField(max_length=254)
    service = forms.ChoiceField(choices=BOOKING_TYPES)

class TeachingForm(forms.Form):
    """
    Step two of form
    """
    address = forms.CharField()
    day = forms.CharField(max_length=32, choices=DAY_OF_WEEK)
    time = forms.TimeField(blank=True, null=True)
    instrument = forms.CharField(max_length=32, choices=INSTRUMENTS)
    description = forms.CharField(max_length=254, blank=True)
