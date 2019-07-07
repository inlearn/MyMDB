#!/usr/bin/env python
# coding:utf-8
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()
from django.contrib.auth.models import User

# user=User.objects.create_user('john','lennon@haha.com','johnpassword')
# user.last_name='lennon'
# user.save()
user=User.objects.get(username='john')
user.set_password('admin')
user.save()
print(user)