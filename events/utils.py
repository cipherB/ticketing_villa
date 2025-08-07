from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.mail import EmailMessage
from django.conf import settings

def generate_ticket_pdf(order_id, name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 100, f"Your Order ID is: #{order_id}")

    # Content
    c.setFont("Helvetica", 12)
    y = height - 160

    c.drawString(72, y, f"Thank you {name} for purchasing a ticket. Please make transaction to:")
    y -= 30

    c.drawString(100, y, f"Account Number: 2066176772")
    y -= 25

    c.drawString(100, y, f"Account Name: Okoroafor Emmanuel")
    y -= 25

    c.drawString(100, y, f"Bank: United Bank of Africa")
    y -= 40

    c.drawString(72, y, "and send a screenshot of your receipt to our contact line")

    # Finalize PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def send_email_with_pdf(to_email, order_id, name):
    try:
        pdf_buffer = generate_ticket_pdf(order_id, name)
        pdf_content = pdf_buffer.read()
        
        subject = "Ticket Purchased!"
        body = f"Hi {name},\n\nThank you for making a purchase.\nPlease find the attached PDF.\n\nRegards,\nTicketing Villa"
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        email.attach(f"ticket_{order_id}.pdf", pdf_content, "application/pdf")
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