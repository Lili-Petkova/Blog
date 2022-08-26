from celery import shared_task

from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(topic, text, from_email, to_email):
    django_send_mail(topic, text, from_email, [to_email])


@shared_task
def contact(text, from_email):
    django_send_mail('Message from user', text, from_email, ['admin@mail.com'])
