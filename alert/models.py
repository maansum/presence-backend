from django.db import models
from accounts.models import User
from groups.models import GroupModel
# Create your models here.
class AlertModel(models.Model):
    message= models.CharField(max_length=100)
    to= models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_to')
    sender= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_sender')
    group= models.ForeignKey(GroupModel,on_delete=models.CASCADE,related_name='group_related',default=1)

    send_at= models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)

def __str__(self):
    return self.sender
                 