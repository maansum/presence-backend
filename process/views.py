from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from process.models import Capture 
from accounts.models import User
from groups.models import GroupModel
from process.serializers import CaptureSerilaizer
from test_attendance import check_attendance
from django.core import serializers

# Create your views here.
# to take attendance the group photo is caputred 


class CaptureView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        group_id = request.data.get('group') 
         # Use request.data.get() to safely get the 'group' field
        #print(user_id,group_id)
        request.data['uploader']= user_id

        # Check if the user is a member of the specified group
        check = GroupModel.objects.filter(id=group_id, creator_id=user_id).exists()

        if not check:
            return Response({'error': 'You cannot proceed for attendance for this group.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CaptureSerilaizer(data=request.data)  # Pass request data to serializer
        if serializer.is_valid():
            serializer.save()
            # path of the image the is being captured for attendance
            group_image_path=serializer.data['captureImage'] 
            # images path that were store in the user model  under profilePic
            student_images=[] 
            
            path= list(User.objects.all().values_list("profilePic")) 
            print("path={}, len={},type={}".format(path,len(path),type(path[0])))
            # for p in path:
            #     print(p)
            student_images=[p[0] for p in path]
            student_images= [ p for p in student_images if len(p)>0 ]
            print("student_images={}, len={},type={}".format(student_images,len(student_images),type(student_images[0])))
            
            
            image_path= check_attendance(group_image_path,student_images)
            print("image path={}".format(image_path))
            
            present_users= User.objects.filter(profilePic__in= image_path)
            present_user_ids = list(present_users.values_list('id', flat=True))
            
            for p in present_user_ids:
                print(p)
            return Response({'message': "Successfully uploaded.",'response':serializer.data, 'present_users':present_user_ids },
                             status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

           
            
           
            

            









           

        

