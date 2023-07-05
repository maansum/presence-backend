from django.db import models
from accounts.models import User
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver

# Create your models here.
class GroupModel(models.Model):
    user= models.ManyToManyField(User, related_name='groups')
    name = models.CharField(max_length=200)
    creator= models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    

    # @receiver(pre_delete, sender=User)
    # def delete_related_groups(sender, instance, **kwargs):
    #     instance.groups.clear()



#creating model for attendees of the group

class Attendees(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_id')
    group=models.ForeignKey(GroupModel,on_delete=models.CASCADE, related_name='group_id')
    action= models.CharField(choices=[('add','Add'),('remove','Remove')], max_length=20,default='add')

    def __str__(self):
        return str(self.group)