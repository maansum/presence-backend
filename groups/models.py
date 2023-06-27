from django.db import models
from accounts.models import User

# Create your models here.
class GroupModel(models.Model):
    user= models.ManyToManyField(User, related_name='groups')
    name = models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)



#creating model for attendees of the group

class Attendees(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_id')
    group=models.ForeignKey(GroupModel,on_delete=models.CASCADE, related_name='group_id')
    action= models.CharField(choices=[('add','Add'),('remove','Remove')], max_length=20,default='add')

    def __str__(self) -> str:
        return super().__str__(self.group)
                            