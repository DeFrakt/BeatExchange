from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first']) < 2:
            errors["first"] = "First name should be at least 2 characters"
        if len(postData['last']) < 2:
            errors["last"] = "Last name should be at least 2 characters"
        if not postData['first'].isalpha():
            errors['first'] = "First name must be alphabetic."
        if not postData['last'].isalpha():
            errors['last'] = "First name must be alphabetic."
        if len(postData['email']) < 10:
            errors["email"] = "Email should be at least 10 characters"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address."
        user = User.objects.filter(email = postData['email'])
        if len(user):
            errors['email'] = "Account already exists for this email."
        if len(postData['pwd']) < 8:
            errors["pwd"] = "Password should be at least 8 characters"
        if postData['pwd'] != postData['pwd_confirm']:
            errors["pwd_confirm"] = "Passwords do not match"
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email_login'])
        # print(user.password)
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email_login']):
            errors['email_log'] = "Invalid email address."
        if len(user) == 0:
            errors['email_log'] = "Could not be logged in."
        elif not bcrypt.checkpw(postData['pwd_login'].encode(), user[0].password.encode()):
            errors['pwd_log'] = "Incorrect password."
        return errors
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    suspend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __str__(self):
        return "ID:" + str(self.id)+ " |F:" + self.first_name + " |L:" + self.last_name + " |E:" + self.email + " |P:" + self.password

class Beat(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='audio/')
    desc = models.TextField(max_length=1000)
    payment = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name = "owner")
    allowed_users = models.ManyToManyField(User, related_name = "allowed_beat")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Sample(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    payment = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name = "user_id")
    allowed_sample = models.ManyToManyField(User, related_name = "allowed")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)





