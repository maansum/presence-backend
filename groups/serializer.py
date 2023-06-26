from rest_framework import serializers
from groups.models import GroupModel
from accounts.serializers import UserLoginSerializer
from accounts.models import User



class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=GroupModel

        fields=['id','name','created_at','user']

    def validate_name(self,value):
            user= self.context['request'].user
            if GroupModel.objects.filter(user=user,name=value).exists():
                raise serializers.ValidationError("A group name already exists, try another")
            return value
    
    #d]hello
                      


#update serializer

class UpdateGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
          model= GroupModel
          fields=['name','user_id']     
          
    def validate_name(self,value):
            user= self.context['request'].user
            if GroupModel.objects.filter(user=user,name=value).exists():
                raise serializers.ValidationError("A group name already exists, try another")
            return value   


#get all user serializer

class AllGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupModel
        fields=['id','name','created_at']


# serializer to delete the group 

# class DeleteGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= GroupModel
#         fields= '__all__'
