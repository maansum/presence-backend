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
          