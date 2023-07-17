from rest_framework import serializers
from rest_framework.response import Response
from attendances.models import Attendance,Picture
from groups.models import Attendees,GroupModel
from accounts.models import User
from django.db.models import Count
import os
from datetime import date
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
                

#MyAttendanceReport serializer

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupModel
        fields=['id','name']



class MyAttendanceReportSerializer(serializers.ModelSerializer):
        group= serializers.SerializerMethodField()
        totalDays=serializers.SerializerMethodField()
        presentDays=serializers.SerializerMethodField()
        class Meta:
            model=Attendance
            fields=['group','totalDays','presentDays']

        def get_group(self,obj):
            id=obj['id']
            group=GroupModel.objects.get(id=id)
            print(group)
            serializer = GroupSerializer(group)
            return serializer.data


        def get_totalDays(self, obj):
          
            id = obj['id']
            totalDays=Attendance.objects.filter(group_id=id).values('date').annotate(total=Count('date')).count()
            return totalDays
        def get_presentDays(self, obj):
            id = obj['id']
            user= self.context['request'].user.id
            present_days=Attendance.objects.filter(group_id=id,present_user_id=user,status=1).values('date').annotate(total=Count('date')).count()
            return present_days

 




 # serializer to get attendance of the attendees in the group that i created



class MyGroupSerializer(serializers.ModelSerializer):
    totalStudent=serializers.SerializerMethodField()
    class Meta:
        model=GroupModel
        fields=['id','name','totalStudent']
    def get_totalStudent(self,obj):
        total=Attendees.objects.filter(group_id=obj.id,).values_list('user_id',flat=True).count()
       
        return total

class MyAttendanceSerializer(serializers.ModelSerializer):
    presentStudent=serializers.SerializerMethodField()
    date=serializers.SerializerMethodField()



    class Meta:
        model=Attendance
        fields=['date','presentStudent']

    def get_presentStudent(self,obj):
        
        present= Attendance.objects.filter(group_id=obj.group_id, date= obj.date,status=1).distinct().count()
       
        return present
    
    def get_date(self,obj):
        dates= Attendance.objects.filter(group_id=obj.group_id).values_list('date',flat=True).distinct()
        return dates.first()


class AttendanceGroupSerializer(serializers.ModelSerializer):
    group=serializers.SerializerMethodField()
    attendance=serializers.SerializerMethodField()


    class Meta:
        model=Attendance
        fields=['group','attendance']
    def get_group(self,obj):
        id=obj.id
        
        user=self.context['request'].user
        
        group=GroupModel.objects.get(id=id)
        serializer=MyGroupSerializer(group,context={'user':user})
        return serializer.data
    
    def get_attendance(self,obj):
        
        groups=Attendance.objects.filter(group_id=obj.id).distinct()
        for g in groups:
            print(g.date)

        serializer=MyAttendanceSerializer(groups,many=True)
        return serializer.data