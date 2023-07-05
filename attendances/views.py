from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from attendances.serializer import AttendanceSerializer
from groups.models import GroupModel
from attendances.models import Attendance
from datetime import date
from django.db.models import Q


# Create your views here.

# view for attendance
class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.data:
            return Response({'error': 'Provide the input details'})

        group_id = int(request.data.get('group'))

        user = request.user.id
        group = GroupModel.objects.get(id=group_id)
        if group.creator_id and user != group.creator_id:
            return Response({'error': 'You cannot take attendance of this group'}, status=status.HTTP_400_BAD_REQUEST)

        if group_id != group.id:
            return Response({'error': 'No such group id found'}, status=status.HTTP_400_BAD_REQUEST)
        
         # Check if attendance has already been taken for today
        today = date.today()
        attendance_exists = Attendance.objects.filter(
            Q(group=group) & Q(date=today)
        ).exists()

        if attendance_exists:
            return Response({'error': 'Attendance  already  taken you can update if need to'}, status=status.HTTP_400_BAD_REQUEST)


        serializer = AttendanceSerializer(data=request.data, context={'request': request} )
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Attendance taken for all users'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

# for updating the attendance 

class AttendanceUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request,format=None):
        if not request.data:
            return Response({'error': 'Provide the input details'})

        group_id = int(request.data.get('group'))
        present_users= request.data.get('present_user')
        stat= request.data.get('status')
        date= request.data.get('date')

        user = request.user.id
        group = GroupModel.objects.get(id=group_id)
        if group.creator_id and user != group.creator_id:
            return Response({'error': 'You cannot take attendance of this group'}, status=status.HTTP_400_BAD_REQUEST)

        if group_id != group.id:
            return Response({'error': 'No such group id found'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            for i in present_users:
                attendance, _ = Attendance.objects.filter(
                present_user=i,
                group=group,
                date=date
            ).update_or_create(
                defaults={'status': stat}
            )
            return Response({'message': 'Attendance updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        




