from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from alert.models import AlertModel
from django.shortcuts import get_object_or_404
from groups.models import GroupModel
from alert.serializer import AlertSerializer,GetAlertSerializer
from accounts.models import User 
from groups.models import Attendees
# Create your views here. notication view 

class AlertView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None ):
        try:
            user = request.user.id
            notifications = AlertModel.objects.filter(to_id=user,read=False)
            serializer = GetAlertSerializer(notifications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            sender= request.user.id
            group_id= request.data['group']
            #print(sender,group_id)
            recipient= GroupModel.objects.filter(id=group_id).values_list('creator_id')
            print(recipient[0][0])
            if sender==recipient[0][0]:
                return Response({'error':'you cannot send request to yourself'},status=status.HTTP_400_BAD_REQUEST)
            request.data['sender']=sender
            request.data['to']=recipient[0][0]

            print(request.data)

            serializer = AlertSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Request Has been Sent','data': serializer.data }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# to accknowledge the notification and to vuew individual notifications
class AlertDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(AlertModel, pk=pk)

    def get(self, request, pk):
        try:
            notification = self.get_object(pk)
            serializer = AlertSerializer(notification)
            return Response(serializer.data)
        except AlertModel.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, pk):
        try:
            notification = self.get_object(pk)
            notification.read = True # Assuming you have a 'read' field in your Alert model
          
            notification.save()
            serializer = AlertSerializer(notification)
            return Response(serializer.data)
        except AlertModel.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
            
