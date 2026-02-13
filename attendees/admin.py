# Register your models here.

# Django doesn't automatically show model, so register to show Attendees in admin dashboard
from django.contrib import admin
from .models import Attendee

# Create a class to customize admin view
class AttendeeAdmin(admin.ModelAdmin):
    # Columns to display in the table
    list_display = ('full_name', 'email', 'registered_at')
    # Sort by newest registered first
    ordering = ('-registered_at',)
    # Add a search bar for these fields
    search_fields = ('first_name', 'last_name', 'email')

    # Method to combine first and last name
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.admin_order_field = 'first_name'  # django sorts by first name

# Register the model with the custom admin
admin.site.register(Attendee, AttendeeAdmin)