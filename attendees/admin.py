# Register your models here.

# django doesn't auto show model, so register to show Attendees in admin dashboard
from django.contrib import admin
from .models import Attendee

# create a class to customize admin view
class AttendeeAdmin(admin.ModelAdmin):
    # columns to display in the table
    list_display = ('full_name', 'email', 'registered_at')
    # sort by newest registered first
    ordering = ('-registered_at',)
    # add a search bar for these fields
    search_fields = ('first_name', 'last_name', 'email')

    # method to combine first and last name
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.admin_order_field = 'first_name'  # django sorts by first name

# register the model with the custom admin
admin.site.register(Attendee, AttendeeAdmin)