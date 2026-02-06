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

# -----------------------------
# PDF helper function
# -----------------------------
from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

def personalize_eticket_from_jpg(jpg_path, name):
    """
    Convert a JPG image to PDF and overlay attendee name.
    Returns a BytesIO object containing the final PDF.
    """
    # -----------------------------
    # Step 1: Convert JPG to PDF
    # -----------------------------
    image = Image.open(jpg_path)
    pdf_bytes = BytesIO()
    image_rgb = image.convert("RGB")  # ensure it's RGB
    image_rgb.save(pdf_bytes, format="PDF")
    pdf_bytes.seek(0)

    # -----------------------------
    # Step 2: Load PDF and prepare overlay
    # -----------------------------
    base_pdf = PdfReader(pdf_bytes)
    page = base_pdf.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # Create overlay with name
    overlay_stream = BytesIO()
    can = canvas.Canvas(overlay_stream, pagesize=(width, height))
    can.setFont("Helvetica", 14)
    can.setFillColorRGB(1, 1, 1)

    # Bottom-left coordinates of name position
    x = 431 
    y = 181 
    can.drawString(x, y, name)
    can.save()
    overlay_stream.seek(0)

    overlay_pdf = PdfReader(overlay_stream)
    output = PdfWriter()

    # Merge overlay onto base PDF
    for i in range(len(base_pdf.pages)):
        page = base_pdf.pages[i]
        if i < len(overlay_pdf.pages):
            page.merge_page(overlay_pdf.pages[i])
        output.add_page(page)

    # Save final PDF to BytesIO
    final_pdf_stream = BytesIO()
    output.write(final_pdf_stream)
    final_pdf_stream.seek(0)
    return final_pdf_stream

# -----------------------------
# Views
# -----------------------------
def register(request):
    if request.method == "POST":
        form = AttendeeForm(request.POST)

        if form.is_valid():
            attendee = form.save()  # Save attendee

            # -----------------------------
            # PDF template path
            # -----------------------------
            # Path to your JPG template
            jpg_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # this points to 'theforum/'
                "attendees",
                "static",
                "attendees",
                "images",
                "eticket_template_2025.jpg"
            )

            # Generate personalized PDF
            pdf_file = personalize_eticket_from_jpg(jpg_path, attendee.first_name)

            # -----------------------------
            # Save PDF to Desktop
            # -----------------------------
            desktop_path = "/Users/aureliatan/desktop"
            output_file = os.path.join(desktop_path, f"{attendee.first_name}_eticket.pdf")

            with open(output_file, "wb") as f:
                f.write(pdf_file.getbuffer())


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
            '''
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.attach(f"{attendee.first_name}_eticket.pdf", pdf_file.read(), "application/pdf")
            msg.send()  # Send email
            '''
            return render(request, 'success.html', {'attendee_email': attendee.email})

    else:
        form = AttendeeForm()

    return render(request, 'register.html', {'form': form})


def success(request):
    return render(request, 'success.html')