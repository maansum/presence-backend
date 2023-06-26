from rest_framework.response import Response
from rest_framework. views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from groups.models import GroupModel
from groups.serializer import GroupSerializer,UpdateGroupNameSerializer,AllGroupSerializer
from rest_framework.exceptions import PermissionDenied, NotFound

# create your views

# for creating group 

class GroupCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serializer= GroupSerializer(data= request.data,context={'request':request})
        if serializer.is_valid(raise_exception= True):
            serializer.save(user=request.user)
            return Response({'message':'group created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# update the name of the group
class UpdateGroupNameView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request, pk):
        try:
            group= GroupModel.objects.get(pk=pk, user=request.user)
        except GroupModel.DoesNotExist:
            # raise NotFound('no such group found')
            return Response({'error':'no group found for provide id'},status=status.HTTP_400_BAD_REQUEST)
        if group.user_id != request.user.id:
            raise PermissionDenied("you can't access that group")
        

        serializer= UpdateGroupNameSerializer(group, data= request.data ,context={'request':request},partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'updated successfully','update':serializer.data},status=status.HTTP_200_OK)
        
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        

# get all the group created by the loggin user

class GetAllGroupCreatedView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request, format=None):
        try:
            groups= GroupModel.objects.filter(user=request.user)
        except GroupModel.DoesNotExist:
            return Response({'messsage':'no group available'})
        serializer= AllGroupSerializer(groups, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
# for deleting the group 

class DeleteGroupView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, pk):
        try:
            group= GroupModel.objects.get(pk=pk, user=request.user)
        except GroupModel.DoesNotExist:
            # raise NotFound('no such group found')
            return Response({'error':'no group found for provide id'},status=status.HTTP_400_BAD_REQUEST)
        if group.user_id != request.user.id:
            raise PermissionDenied("you can't access that group")

        group.delete()

        return Response({'message':'deleted successfully'})


    
                     