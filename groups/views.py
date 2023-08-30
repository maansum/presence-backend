from rest_framework.response import Response
from rest_framework. views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from groups.models import GroupModel,Attendees
from accounts.models import User
from groups.serializer import GroupSerializer,UpdateGroupNameSerializer,AllGroupSerializer,AttendeesSerializer,InvolvementSerializer
from rest_framework.exceptions import PermissionDenied
from accounts.serializers import AllUserSerializer
from django.db import transaction
from django.db.models import Q 

# create your views

# for creating group 

class GroupCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serializer= GroupSerializer(data= request.data,context={'request':request})
        if serializer.is_valid(raise_exception= True):
            serializer.save(creator=request.user)
            return Response({'message':'group created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# update the name of the group
class UpdateGroupNameView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request, pk):
        try:
            group= GroupModel.objects.get(pk=pk, creator=request.user)
        except GroupModel.DoesNotExist:
            # raise NotFound('no such group found')
            return Response({'error':'no group found for provide id'},status=status.HTTP_400_BAD_REQUEST)
        if group.creator_id != request.user.id:
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
            groups= GroupModel.objects.filter(creator=request.user)
        except GroupModel.DoesNotExist:
            return Response({'messsage':'no group available'})
        serializer= AllGroupSerializer(groups, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
# for deleting the group 

class DeleteGroupView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, pk):
        try:
            group= GroupModel.objects.get(pk=pk, creator=request.user)
        except GroupModel.DoesNotExist:
            # raise NotFound('no such group found')
            return Response({'error':'no group found for provide id'},status=status.HTTP_400_BAD_REQUEST)
        if group.creator_id != request.user.id:
            raise PermissionDenied("you can't access that group" )

        group.delete()

        return Response({'message':'deleted successfully'})
 


# view for attendees adding and removing

class AttendeesView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        action= request.data.get('action')
        user_ids= request.data.get('user',[])
        group_id= request.data.get('group')
         # Validate User ID

        
        user_exists = User.objects.filter(id__in=user_ids).exists()
        if not user_exists:
            return Response({'user may not be register'}, status=status.HTTP_400_BAD_REQUEST)
        
        

        # Validate Group ID
        group_exists = GroupModel.objects.filter(id=group_id).exists()
        if not group_exists:
            return Response({'error': 'Invalid group ID'}, status=status.HTTP_400_BAD_REQUEST)

        #serializer = AttendeesSerializer(data=request.data,many=True)
        if action.lower()=='add': 
            with transaction.atomic():
                existing_attendees = Attendees.objects.filter(user_id__in=user_ids, group_id=group_id).exists()
                if existing_attendees:
                    return Response({'message':'User already present'},status=status.HTTP_400_BAD_REQUEST)

                #existing_user_ids = {attendee.user_id for attendee in existing_attendees}
                new_attendees=[]
                # for user_id in user_ids:
                #     new_attendees.append(user_id)

                new_attendees = [Attendees(user_id=user_id, group_id=group_id) for user_id in user_ids]


                Attendees.objects.bulk_create(new_attendees)

            return Response({'message': 'Users added successfully'}, status=status.HTTP_200_OK)


                        
            
        
        # if action.lower() =='add':

        #     #for checking the user if he or she already added

        #     check= Attendees.objects.filter(user_id=user_id,group_id=group_id).exists()
        #     if check:
        #         return Response({'message':'user already added in the group'},status=status.HTTP_400_BAD_REQUEST)
           
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         return Response({'message':'added successfully', 'details':serializer.data}, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        elif action.lower()=='remove':
           
            try:
                attendee= Attendees.objects.get(user_id=user_ids,group_id=group_id)
                attendee.delete()
                return Response({'message':'successfully deleted'},status=status.HTTP_200_OK)
            

            except Attendees.DoesNotExist:
                return Response({'error':'No such details found'},status=status.HTTP_404_NOT_FOUND)
            

        return Response({'error':'invalid action'},status=status.HTTP_400_BAD_REQUEST)



# for getting the attendees of the group

class AttendeesOfGroup(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        group_id=pk
        if group_id is None:
            return Response({'error':'group id is essential'},status=status.HTTP_400_BAD_REQUEST)

        users=Attendees.objects.filter(group_id=group_id).values('user_id')
        user_ids = [user['user_id'] for user in users]
        attendees=User.objects.filter(id__in=user_ids)
        serializer= AllUserSerializer(attendees,many=True)

        return Response({
            'group':group_id,
            'attendees': serializer.data})
    


# for getting the group where the user is involves 

class InvolvedGroupView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
            try:
                user= request.user.id
            

                attendedGroups= Attendees.objects.filter(user_id=user)
                group_ids= attendedGroups.values_list('group_id',flat=True)

                groups= GroupModel.objects.filter(id__in=group_ids)

                serializer= InvolvementSerializer(groups, many=True)
                return Response({'involvement':serializer.data})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     

            
# for recommendation of the group to their home page except their groups

class RecommendedView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        user_id= request.user.id

        try:
            attendees_group=Attendees.objects.exclude(user_id=user_id).values('group_id')
            groups= GroupModel.objects.exclude(Q(creator_id=user_id) & Q(id__in=attendees_group)
            )


        except GroupModel.DoesNotExist:
            return Response({'messsage':'no group available'},status=status.HTTP_400_BAD_REQUEST)
        serializer= AllGroupSerializer(groups, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




    
                     