from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, VisitorRegistration
from django.forms.widgets import PasswordInput, TextInput

from django import forms


# Login Form
class LoginForm(AuthenticationForm):
        username = forms.CharField(widget=TextInput())
        password = forms.CharField(widget=PasswordInput())


#from django import forms
from datetime import timedelta
from .models import VisitorRegistration

class VisitorsForm(forms.ModelForm):
    CIVIL_SERVANT_CHOICES = (
        (True, 'Haa'),
        (False, 'Maya'),
    )

    civil_servant = forms.TypedChoiceField(
        label='Shaqaale rayid?',
        choices=CIVIL_SERVANT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        coerce=lambda x: x == 'True',
        initial=False
    )

    # Override the hours_to_stay field to be a CharField for HH:MM input
    hours_to_stay = forms.CharField(
        required=False,
        label='Duration of Stay (HH:MM)',
        help_text="Enter duration as HH:MM (e.g. 1:20 for 1 hour 20 minutes)",
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM'})
    )

    class Meta:
        model = VisitorRegistration
        fields = [
            'full_name', 'phone_number', 'civil_servant',
            'person_to_visit', 'visit_reason', 'hours_to_stay'
        ]
        labels = {
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'person_to_visit': 'Office to Visit',
            'visit_reason': 'Reason for Visit',
            # 'hours_to_stay' label overridden above
        }

    def clean_hours_to_stay(self):
        data = self.cleaned_data.get('hours_to_stay')
        if not data:
            return None
        try:
            parts = data.split(':')
            if len(parts) != 2:
                raise forms.ValidationError("Fadlan geli waqtiga qaabka saacadaha iyo daqiiqadaha, tusaale: 1:20")
            hours = int(parts[0])
            minutes = int(parts[1])
            if hours < 0 or minutes < 0 or minutes >= 60:
                raise forms.ValidationError("Fadlan geli saacado iyo daqiiqado sax ah")
            return timedelta(hours=hours, minutes=minutes)
        except (ValueError, IndexError):
            raise forms.ValidationError("Fadlan geli waqtiga qaabka saacadaha iyo daqiiqadaha, tusaale: 1:20")
