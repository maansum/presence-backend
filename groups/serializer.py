from rest_framework import serializers
from groups.models import GroupModel,Attendees,User
from accounts.serializers import UserLoginSerializer, UserRegistrationSerializer
from accounts.models import User



class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=GroupModel

        fields=['id','name','created_at']

    def validate_name(self,value):
            user= self.context['request'].user
            if GroupModel.objects.filter(creator=user,name=value).exists():
                raise serializers.ValidationError("A group name already exists, try another")
            return value
    
    
                      


#update serializer

class UpdateGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
          model= GroupModel
          fields=['name','creator_id']     
          
    def validate_name(self,value):
            user= self.context['request'].user
            if GroupModel.objects.filter(creator=user,name=value).exists():
                raise serializers.ValidationError("A group name already exists, try another")
            return value   


#get all user serializer

class AllGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupModel
        fields=['id','name','created_at','creator']


#serializer for attendees

class AttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendees
        fields=['action','user','group']


#serializer for showing the group involves 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','phoneNumber']

     




class InvolvementSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        user_ids = Attendees.objects.filter(group_id=obj.id).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids)
        serializer = UserSerializer(users, many=True)
        return serializer.data

    class Meta:
        model = GroupModel
        fields = ['id', 'name', 'created_at', 'creator', 'users']
    



          