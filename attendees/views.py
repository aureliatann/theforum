# Create your views here.
from django.shortcuts import render, redirect
from .forms import AttendeeForm

# email function imports
from django.core.mail import send_mail
from django.conf import settings

# view -> python function that runs when someone opens a webpage (when use visits this URL, what should website do?)

# this view / function runs whenever someone visits registration page
def register(request):
    # if POST (user just submitted the form), need to process and save form
    if request.method == "POST":
        form = AttendeeForm(request.POST)   # loads the dat athe user typed into django form
        # django checks that name isn't empty and email is in valid format
        if form.is_valid():
            attendee = form.save()  # save and get instance

            # SEND EMAIL
            send_mail(
            subject='Registration Confirmation – The Forum 2026',
            message=f"""Dear {attendee.first_name},
            
            We are pleased to confirm your registration for The Forum 2026. Your e-ticket is attached below.
            
            Here are the event details for your reference:
            
            🗓️ Date: Sunday, April 12, 2026
            ⏱️ Open Gate: 5:00 PM AEST
            📍 Location: Copland Theatre (B01), The Spot, The University of Melbourne
            
            We look forward to seeing you at the event and hope you enjoy an engaging and insightful experience.
            If you have any questions or require further assistance, please feel free to reach out to us anytime.
            
            Best regards,
            The Forum Team
            """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[attendee.email],
                fail_silently=False,
            )
            # EMAIL SENT

            return render(request, 'success.html', {'attendee_email': attendee.email})
    else:
        # user's first time visiting (GET request) -> show empty form
        form = AttendeeForm()

    # render -> show the register HTML
    return render(request, 'register.html', {'form': form})

# when form is saved, show the success HTML
def success(request):
    return render(request, 'success.html')