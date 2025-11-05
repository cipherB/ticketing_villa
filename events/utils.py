from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue
from django.core.mail import EmailMessage
from django.conf import settings

def generate_purchased_ticket_pdf(purchased_ticket, order):
    """Generate PDF for a single purchased ticket with enhanced styling"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Colors
    brand_blue = blue
    dark_gray = (0.2, 0.2, 0.2)
    light_gray = (0.9, 0.9, 0.9)
    
    # Draw header background
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(0, height - 120, width, 120, fill=1, stroke=0)
    
    # Company branding
    c.setFillColor(brand_blue)
    c.setFont("Helvetica-Bold", 24)
    title_text = "TICKETING VILLA"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 24)
    c.drawString((width - title_width) / 2, height - 50, title_text)
    
    c.setFillColorRGB(*dark_gray)
    c.setFont("Helvetica", 12)
    subtitle_text = "Your Premium Event Ticket"
    subtitle_width = c.stringWidth(subtitle_text, "Helvetica", 12)
    c.drawString((width - subtitle_width) / 2, height - 75, subtitle_text)
    
    # Draw a decorative line
    c.setStrokeColor(brand_blue)
    c.setLineWidth(2)
    c.line(72, height - 100, width - 72, height - 100)
    
    # Starting Y position for content
    y = height - 150

    # Personal greeting with enhanced styling
    c.setFillColorRGB(*dark_gray)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, f"Hello {order.full_name},")
    y -= 25
    
    c.setFont("Helvetica", 12)
    c.drawString(72, y, "Your digital ticket is ready! Please present this at the event entrance.")
    y -= 50

    # Order Details section with background box
    box_y = y - 10
    c.setFillColorRGB(*light_gray)
    c.rect(50, box_y - 280, width - 100, 280, fill=1, stroke=0)
    
    # Order Details header
    c.setFillColor(brand_blue)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "📋 TICKET DETAILS")
    y -= 35

    # Reset color for content
    c.setFillColorRGB(*dark_gray)
    
    # Order Number with emphasis
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Order Number:")
    c.setFont("Helvetica", 12)
    c.drawString(180, y, f"#{order.id}")
    y -= 25
    
    # Ticket ID - Most important for verification
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(brand_blue)
    c.drawString(72, y, "🎫 TICKET ID:")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, f"{purchased_ticket.unique_id}")
    y -= 35
    
    # Event details section
    c.setFillColorRGB(*dark_gray)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Event:")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(130, y, f"{purchased_ticket.ticket.event.name}")
    y -= 25
    
    # Date and time on same line
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Date & Time:")
    c.setFont("Helvetica", 12)
    c.drawString(150, y, f"{purchased_ticket.ticket.event.event_date} at {purchased_ticket.ticket.event.event_time}")
    y -= 25
    
    # Venue information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Venue:")
    venue_info = purchased_ticket.ticket.event.venue_name or "Venue TBA"
    c.setFont("Helvetica", 12)
    c.drawString(120, y, venue_info)
    y -= 20
    
    # Address with proper formatting
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Address:")
    c.setFont("Helvetica", 11)
    
    # Handle long addresses by wrapping
    address = purchased_ticket.ticket.event.address
    max_width = 400
    if len(address) > 50:
        words = address.split()
        lines = []
        current_line = ""
        for word in words:
            if c.stringWidth(current_line + " " + word, "Helvetica", 11) < max_width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            c.drawString(130, y - (i * 12), line)
        y -= len(lines) * 12 + 8
    else:
        c.drawString(130, y, address)
        y -= 25
    
    # Ticket type and category
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Ticket Type:")
    c.setFont("Helvetica", 12)
    c.drawString(160, y, purchased_ticket.ticket.name)
    y -= 20
    
    if purchased_ticket.ticket.event.category:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, "Category:")
        c.setFont("Helvetica", 12)
        c.drawString(140, y, purchased_ticket.ticket.event.get_category_display())
        y -= 25
    
    # Buyer information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Purchased by:")
    c.setFont("Helvetica", 12)
    c.drawString(170, y, order.full_name)
    y -= 50

    # Important notice section with border
    notice_y = y - 10
    c.setStrokeColorRGB(0.8, 0.2, 0.2)  # Red border
    c.setLineWidth(2)
    c.rect(50, notice_y - 60, width - 100, 60, fill=0, stroke=1)
    
    # Warning message
    c.setFillColorRGB(0.8, 0.1, 0.1)  # Red text
    c.setFont("Helvetica-Bold", 14)
    warning_text = "⚠️ IMPORTANT NOTICE"
    warning_width = c.stringWidth(warning_text, "Helvetica-Bold", 14)
    c.drawString((width - warning_width) / 2, y - 25, warning_text)
    c.setFont("Helvetica-Bold", 12)
    notice_text = "Do not share this ticket with anyone!"
    notice_width = c.stringWidth(notice_text, "Helvetica-Bold", 12)
    c.drawString((width - notice_width) / 2, y - 45, notice_text)
    y -= 80

    # Footer section
    c.setFillColorRGB(*dark_gray)
    c.setFont("Helvetica", 11)
    footer_text = "Thank you for choosing Ticketing Villa for your event experience."
    footer_width = c.stringWidth(footer_text, "Helvetica", 11)
    c.drawString((width - footer_width) / 2, y, footer_text)
    y -= 20
    
    c.setFont("Helvetica-Bold", 12)
    contact_text = "Need help? Contact us at support@ticketingvilla.com"
    contact_width = c.stringWidth(contact_text, "Helvetica-Bold", 12)
    c.drawString((width - contact_width) / 2, y, contact_text)
    y -= 30
    
    # Bottom branding
    c.setFillColor(brand_blue)
    c.setFont("Helvetica-Bold", 10)
    brand_text = "TICKETING VILLA - Premium Event Experiences"
    brand_width = c.stringWidth(brand_text, "Helvetica-Bold", 10)
    c.drawString((width - brand_width) / 2, y, brand_text)
    
    # Draw decorative bottom line
    c.setStrokeColor(brand_blue)
    c.setLineWidth(1)
    c.line(72, y - 15, width - 72, y - 15)

    # Finalize PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def send_email_with_purchased_tickets(to_email, order, purchased_tickets):
    """Send email with individual PDF for each purchased ticket"""
    try:
        subject = "Tickets Purchased!"
        body = f"Hi {order.full_name},\n\nThank you for making a purchase.\nPlease find your tickets attached as individual PDF files.\n\nRegards,\nTicketing Villa"
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        
        # Generate and attach PDF for each purchased ticket
        for purchased_ticket in purchased_tickets:
            pdf_buffer = generate_purchased_ticket_pdf(purchased_ticket, order)
            pdf_content = pdf_buffer.read()
            
            # Create unique filename with purchased ticket unique_id
            filename = f"ticket_{purchased_ticket.unique_id}.pdf"
            email.attach(filename, pdf_content, "application/pdf")
        
        email.send()
        
    except Exception as e:
        # Log the error and handle appropriately
        print(f"Error sending email: {e}")
        raise
    
def notify_admin_of_purchase(to_email, order_id, full_name):
    try:
        subject = f"[New Order] Ticket Purchased - #{order_id}"
        message = f"""
        A new ticket has just been purchased.

        Name: {full_name}
        Customer Email: {to_email}
        Order ID: #{order_id}

        Log in to the admin panel for more details.
            """.strip()

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],  # Sends to yourself
        )
        email.send()

    except Exception as e:
        print(f"Error sending admin notification email: {e}")