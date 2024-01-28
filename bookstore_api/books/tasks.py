from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from books.models import CartItem

@shared_task(bind=True)
def send_purchase_notification(self, email, cart_item_ids):
    """
    Task for sending purchase notification email to the user.
    """
    # Retrieve cart items using primary keys
    cart_items = CartItem.objects.filter(id__in=cart_item_ids)
    
    total = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)
    
    # Prepare email subject and message
    subject = 'Purchase Confirmation'
    message = render_to_string('purchase_email_template.html', {'items': cart_items, "total": total})
    
    # Send email using send_mail function
    send_mail(subject, message, from_email=None, recipient_list=[email], html_message=message)
    
    cart_items.delete()
    
    return "Email is sent"
