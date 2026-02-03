from django.contrib import admin

# Register your models here.

# django doesn't auto show model, so register to show Attendees in admin dashboard
from .models import Attendee
admin.site.register(Attendee)