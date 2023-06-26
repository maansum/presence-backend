from django.db import models
from accounts.models import User

# Create your models here.
class GroupModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)



