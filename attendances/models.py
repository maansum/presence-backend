from django.db import models
from accounts.models import User
from groups.models import GroupModel
import os

# Create your models here.
#  attendance model

class Attendance(models.Model):
    present_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='present_user')
    group=models.ForeignKey(GroupModel,on_delete=models.CASCADE)
    date= models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)


    def __str__(self):
        return self.group
    

# to save photo for attendance
def get_upload_path(instance, filename):
    group_id=instance.group.id
    return os.path.join('pictures',str(group_id),filename)

class Picture(models.Model):
    group=models.ForeignKey(GroupModel,on_delete=models.CASCADE)
    photoPath=models.ImageField(upload_to=get_upload_path)
                                  
    date=models.DateField(auto_now_add=True)



    
