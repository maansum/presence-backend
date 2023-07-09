from rest_framework import serializers
from rest_framework.response import Response
from attendances.models import Attendance,Picture
from groups.models import Attendees
from accounts.models import User
import os
# from accounts.serializers import UserRegistrationSerializer




# attendance serializer 


class AttendanceSerializer(serializers.ModelSerializer):
    present_user = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Attendance
        fields = ['group', 'present_user', 'date', 'status']

    def create(self, validated_data):
        present_users = validated_data.pop('present_user', [])
        group=validated_data['group']
        attendance_instances = []

        for user_id in present_users:
            if Attendees.objects.filter(group=group,user_id=user_id).exists:
                user = User.objects.get(id=user_id)
                attendance = Attendance(group=validated_data['group'], present_user=user, status=validated_data['status'])
                attendance_instances.append(attendance)
            else:
                return Response(f"user:{user_id} is not the attendee of the group:{group}")

        Attendance.objects.bulk_create(attendance_instances)

        return attendance_instances
    
#make user serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email']

# get attendance seriaizer
class GetAttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = ['present_user']

    # def get_present_user(self, attendance):
    #     user_ids = attendance.values_list('present_user_id', flat=True)
    #     users = User.objects.filter(id__in=user_ids)
    #     return users


# serializer for attendance photos

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model= Picture
        fields=['group','photoPath','date']
    def update(self, instance, validated_data):
        instance.photoPath = validated_data.get('photoPath', instance.photoPath)
        instance.save()
        return instance


        

    
# serialzer for showing the attendance of the present user 
class GetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['id','email','name','phoneNumber'] 
                