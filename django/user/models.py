from django.db import models
from django.contrib.auth.models import User


# 这个模型是用户的详细信息
class UserProfile(models.Model):
    name = models.CharField(max_length=140, blank=True, null=True)
    phone= models.PositiveIntegerField(blank=True,null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
