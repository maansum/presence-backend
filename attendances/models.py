from django.db import models
from accounts.models import User
from groups.models import GroupModel

# Create your models here.
#  attendance model

class Attendance(models.Model):
    present_user=models.ForeignKey(User,on_delete=models.CASCADE)
    group=models.ForeignKey(GroupModel,on_delete=models.CASCADE)
    date= models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)


    def __str__(self):
        return self.group