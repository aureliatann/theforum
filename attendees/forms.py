from django import forms
from .models import Attendee

# Create form based on the Attendee model
# forms.ModelForm -> create form automatically from database model
class AttendeeForm(forms.ModelForm):

    # Meta tells django what model and fields form uses (configuration section)
    class Meta:
        model = Attendee  # Use Attendee model
        fields = ['first_name', 'last_name', 'email'] # Only show name and email in form
        # Widgets lets customize each field's HTML
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-input'
            }),
        }