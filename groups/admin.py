from django.contrib import admin
from groups.models import GroupModel,Attendees

# Register your models here.
admin.site.register(GroupModel)
admin.site.register(Attendees)

