# Create your views here.
from django.shortcuts import render, redirect
from .forms import AttendeeForm

# Email imports
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# PDF imports
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white
from io import BytesIO
import os

# =============================
# Function: personalize_eticket_from_pdf
# Creates a personalized PDF e-ticket by overlaying the attendee's name
# =============================
def personalize_eticket_from_pdf(pdf_path, name):
    # Read base PDF template and use the first page
    base_pdf = PdfReader(pdf_path)
    page = base_pdf.pages[0]

    # Get PDF page dimensions for correct overlay sizing
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # Create a ReportLab canvas the same size as the PDF page (overlay)
    overlay_stream = BytesIO()
    can = canvas.Canvas(overlay_stream, pagesize=(width, height))

   # Set attendee name's font style, size, color, and position
    can.setFont("Helvetica", 14)
    can.setFillColor(white)
    # Coordinates for where the name appears (bottom-left is 0,0)
    x = 266
    y = 165

    # Draw the attendee's name on the overlay
    can.drawString(x, y, name)
    can.save() # Finish the overlay PDF
    overlay_stream.seek(0)  # Move the pointer back to the start so we can read ENTIRE overlay later

    # Read the overlay PDF
    overlay_pdf = PdfReader(overlay_stream)
    # Merge overlay PDF onto base PDF
    output = PdfWriter() # Create a new PDF writer for the final PDF
    base_page = base_pdf.pages[0] # First page of base PDF
    overlay_page = overlay_pdf.pages[0] # First page of overlay PDF
    base_page.merge_page(overlay_page) # Merges base and overlay page
    output.add_page(base_page) # Adds the merged page into final PDF file

    # Save and return PDF
    final_pdf = BytesIO() # Create a BytesIO object to save the final PDF in memory (not writing to disk)
    output.write(final_pdf) # Write the merged PDF to the in-memory file
    final_pdf.seek(0) # Move the pointer back to the start so we can read ENTIRE PDF later
    return final_pdf

# =============================
# View: register
# Handles attendee form submission, PDF generation, and sending confirmation email
# =============================
def register(request):
    # Populate form with POST data (POST request means user submitted the registration form)
    if request.method == "POST":
        form = AttendeeForm(request.POST)

        if form.is_valid():
            attendee = form.save() # Save attendee to database

            # Define path to PDF template
            app_dir = os.path.dirname(os.path.abspath(__file__))
            pdf_path = os.path.join(
                app_dir,
                "static",
                "attendees",
                "pdf",
                "eticket_template_2026.pdf"
            )

            # Generate personalized PDF e-ticket
            pdf_file = personalize_eticket_from_pdf(pdf_path, attendee.first_name)

            # Email details (subject, sender, and recipient)
            subject = "Registration Confirmation – The Forum 2026"
            from_email = settings.EMAIL_HOST_USER
            to = attendee.email

            # Plain text version of the email (fallback)
            text_content = f"""
Dear {attendee.first_name},

Thank you for registering for The Forum 2026.
Your e-ticket is attached below.

Event Details:
- Location: Copland Theatre (B01), The Spot, University of Melboure
- Date: Friday, April 10, 2026
- Open Gate: 5:00 PM AEST
- Dresscode: Batik / Formal

Best regards,
The Forum Team
"""

            # HTML email content (properly formatted)
            html_content = f"""
<p>Dear <strong>{attendee.first_name}</strong>,</p>

<p>
We are pleased to confirm your registration for
<strong>The Forum 2026</strong>. Your e-ticket is attached below.
</p>

<p><strong>Here are the event details for your reference:</strong></p>

<ul>
    <li><strong>📍 Location:</strong> Copland Theatre (B01), The Spot, University of Melboure</li>
    <li><strong>🗓️ Date:</strong> Friday, April 10, 2026</li>
    <li><strong>⏱️ Open Gate:</strong> 5:00 PM AEST</li>
    <li><strong>👔 Dresscode:</strong> Batik / Formal</li>
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

            # Build and send email with PDF attached
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to]) # Creates email object of multiple formats (plain text, HTML, attachments)
            msg.attach_alternative(html_content, "text/html") # Attach HTML version
            msg.attach(f"{attendee.first_name}_eticket.pdf", pdf_file.read(), "application/pdf") # Attach PDF e-ticket
            msg.send()  # Send email
            return render(request, 'success.html', {'attendee_email': attendee.email})

    else:
        # If GET request (user did not submit form), show empty registration form
        form = AttendeeForm()

    # Render the registration form page
    return render(request, 'register.html', {'form': form})

# =============================
# View: success
# Displays success page after registration
# =============================
def success(request):
    return render(request, 'success.html')