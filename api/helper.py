from django import template
from django.conf import settings
from django.http.response import HttpResponse
from rest_framework.exceptions import APIException
from .models import UserLogs
from django.contrib.auth.models import *
from rest_framework.pagination import PageNumberPagination
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
import random


class UserLogHelper():
    def createLog(log, tag, user_id):
        user = User.objects.get(pk = user_id)
        user_log = UserLogs()
        user_log.fk_userid = user
        user_log.log = log 
        user_log.tag = tag
        user_log.save()
        return  


class ResponsePaginationHelper(PageNumberPagination):
    page_query_param = 'page'
    page_size = 100
    page_size_query_param = page_size
    max_page_size = 100 


class GeneratePassword():
    def random_password():
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        password_length = 10
        password = ""

        for i in range(password_length):
            next_index = random.randrange(len(alphabet))
            password = password + alphabet[next_index]
        return password


class AddUserGroups():
    def userGroups(user_groups, user):
        for user_group in user_groups:
            user.groups.add(user_group)
        return True   


class SendEmail():
    def sampleEmail(email):
        email = EmailMessage('Subject', 'Hello Guys', to=[email])
        email.send()

    def UserRegistration(user):
        with open(settings.BASE_DIR / "api/templates/user_registration_email.txt") as txt_message:
            user_registration_message = txt_message.read()+" Username: "+user.username+" Email: "+user.email
        email_message = EmailMultiAlternatives('User Account Confirmation', user_registration_message, 'no-reply@example.com', to=[email])
        html_templete = get_template("user_registration_email.html").render({'username':user.username, 'email':user.email})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()

    def PasswordRest(user):
        with open(settings.BASE_DIR / "api/templates/password_reset_email.txt") as txt_message:
            user_registration_message = txt_message.read()+" Username: "+user.username+" Email: "+user.email
        email_message = EmailMultiAlternatives('Password Reset', user_registration_message, 'no-reply@example.com', to=[user.email])
        html_templete = get_template("password_reset_email.html").render({'username':user.username, 'email':user.email})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()  

    def NewUser(request, password):
        with open(settings.BASE_DIR / "api/templates/new_user_email.txt") as txt_message:
            user_registration_message = txt_message.read()+" Username: "+request['username']+" Email: "+request['email']
        email_message = EmailMultiAlternatives('DRF Base API Account', user_registration_message, 'no-reply@example.com', to=[request['email']])
        html_templete = get_template("new_user_email.html").render({'username':request['username'], 'password': password, 'email':request['email']})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()                  