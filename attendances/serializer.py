from rest_framework import serializers
from rest_framework.response import Response
from attendances.models import Attendance
from groups.models import Attendees
from accounts.models import User




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

