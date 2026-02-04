# Create your views here.
from django.shortcuts import render, redirect
from .forms import AttendeeForm

# Email imports
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# PDF imports
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os

def register(request):
    if request.method == "POST":
        form = AttendeeForm(request.POST)

        if form.is_valid():
            attendee = form.save()  # Save attendee

            # -----------------------------
            # Load PDF template (no writing, no PyPDF2)
            # -----------------------------
            template_path = os.path.join(
                settings.BASE_DIR,
                "attendees",
                "static",
                "attendees",
                "pdfs",
                "eticket_template_2025.pdf"
            )

            if not os.path.exists(template_path):
                raise FileNotFoundError(f"PDF template not found at {template_path}")

            # Read PDF as raw bytes
            with open(template_path, "rb") as f:
                pdf_bytes = f.read()

            # -----------------------------
            # Email subject + sender + recipient
            # -----------------------------
            subject = "Registration Confirmation – The Forum 2026"
            from_email = settings.EMAIL_HOST_USER
            to = attendee.email

            # Plain text fallback
            text_content = f"""
Dear {attendee.first_name},

Thank you for registering for The Forum 2026.
Your e-ticket is attached below.

Event Details:
- Date: Sunday, April 12, 2026
- Open Gate: 5:00 PM AEST
- Location: Copland Theatre (B01), The Spot, The University of Melbourne

Best regards,
The Forum Team
"""

            # HTML email content
            html_content = f"""
<p>Dear <strong>{attendee.first_name}</strong>,</p>

<p>
We are pleased to confirm your registration for 
<strong>The Forum 2026</strong>. Your e-ticket is attached below.
</p>

<p><strong>Here are the event details for your reference:</strong></p>

<ul>
    <li><strong>🗓️ Date:</strong> Sunday, April 12, 2026</li>
    <li><strong>⏱️ Open Gate:</strong> 5:00 PM AEST</li>
    <li><strong>📍 Location:</strong> Copland Theatre (B01), The Spot,<br>
        The University of Melbourne</li>
</ul>

<p>
If you have any questions or require further assistance, 
please feel free to contact us anytime.
</p>

<p>
We look forward to seeing you at the event and hope you enjoy an 
engaging and insightful experience.
</p>

<p>
Warm regards,<br>
<strong>The Forum Team</strong>
</p>
"""

            # -----------------------------
            # Build and send email with PDF attached
            # -----------------------------
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.attach(f"{attendee.first_name}_eticket.pdf", pdf_bytes, "application/pdf")
            msg.send()  # Send email

            return render(request, 'success.html', {'attendee_email': attendee.email})

    else:
        form = AttendeeForm()

    return render(request, 'register.html', {'form': form})


def success(request):
    return render(request, 'success.html')