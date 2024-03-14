from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n'\
        f'You have successfully placed an order.'\
        f'Your order ID is {order.id}'
    mail_sent = send_mail(
        subject, message, 'fmg3ckali@gmail.com', [order.email])
    return mail_sent


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully paid
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n'\
        f'You have successfully completed payment of your order.'\
        f'Your order ID is {order.id} with payment id {order.stripe_id}'
    mail_sent = send_mail(
        subject, message, 'fmg3ckali@gmail.com', [order.email])
    return mail_sent
