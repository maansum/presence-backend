from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from attendances.serializer import AttendanceSerializer,PictureSerializer,GetAttendanceSerializer
from groups.models import GroupModel
from attendances.models import Attendance
from datetime import date
from django.db.models import Q
from accounts.models import User


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

        


# to get attendance of the group of any day

class GetAttendanceView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, format=None):
        
        group_id= request.data.get('group')
        date= request.data.get('date')
    
        try:
            group = GroupModel.objects.get(id=group_id)
        except GroupModel.DoesNotExist:
            return Response({'error': 'No such group id found'}, status=status.HTTP_400_BAD_REQUEST)

        if group.creator_id != request.user.id:
            return Response({'error': 'You cannot access attendance records of this group'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        attendance= Attendance.objects.filter(group_id=group_id,date=date, status=1)
        if not attendance.exists():
            return Response({'error':'no any details'},status=status.HTTP_204_NO_CONTENT)
        
        
        present_user_ids = attendance.values_list('present_user_id',flat=True)
        present_users= User.objects.filter(id__in=present_user_ids)# id__in to deal with list 
        serializer=GetAttendanceSerializer(present_users,many=True)
        return Response({'group':group_id,'present_user': serializer.data}, status=status.HTTP_200_OK)
        





#to get the records of the user 

# class RecordsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user_id = request.user.id
#         # Find the groups where the user_id is an attendee
#         groups = GroupModel.objects.filter(attendees__user_id=user_id)
        
#         group_names = [group.name for group in groups]
#         return Response({'groups': group_names})
                
                


# view for photoPosting


class PictureView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request, format=None):
        user= request.user
        serializer= PictureSerializer( data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user_id':user.id,'profile':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
         





         



