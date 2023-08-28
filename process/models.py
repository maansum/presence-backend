from django.db import models
from accounts.models import User
from groups.models import GroupModel
import os


# Create your models here. for storing the photo taken for attendance

def get_upload_path(instance, filename):
    return os.path.join('attendance',str(instance.group_id),filename)

class Capture(models.Model):
    captureImage=models.ImageField(upload_to=get_upload_path, null=True, blank=False)
    uploader=models.ForeignKey(User, on_delete=models.CASCADE,related_name='attendance_taker')
    group= models.ForeignKey(GroupModel, on_delete=models.CASCADE,related_name='group_capturer')
    created_at= models.DateField(auto_now_add=True)


    def __str__(self):
        return self.captureImage
                                 
