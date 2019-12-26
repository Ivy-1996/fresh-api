# import django
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreshApi.develop')
#
# django.setup()

from django.core.mail import send_mail
from django.conf import settings

from celery import Celery

DOMAIN = getattr(settings, 'DOMAIN', 'http://127.0.0.1:8000')

BROKER = getattr(settings, 'BROKER', 'redis://127.0.0.1:6379/5')

app = Celery('tasks.task', broker=BROKER)

"""发邮件的时候请设置debug为False"""


@app.task
def send_register_mail(to_email, username, token):
    """def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):"""
    subject = '生鲜商城欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>{}, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="{}/user/active/{}" style="color: green">点击激活</a>'.format(
        username, DOMAIN, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
