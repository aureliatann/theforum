from django import forms
from .models import Attendee

# create form based on the Attendee model
# forms.ModelForm -> create form automatically from database model
class AttendeeForm(forms.ModelForm):

    # meta tells django what model and fields form uses (configuration section)
    class Meta:
        model = Attendee            # use Attendee model
        fields = ['name', 'email']  # only show name and email in form