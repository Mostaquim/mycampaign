from django.db import models
from accounts.models import User
# Create your models here.

class Messages(models.Model):
    subject = models.CharField(max_length=100,null=True,blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
    message = models.TextField(null=True,blank=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)