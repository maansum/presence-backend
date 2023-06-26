from rest_framework import serializers
from accounts.models import User
# from accounts.models import UserProfilePic



# Registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},
                                      write_only=True)
    class Meta:
        model= User
        fields=['id','email','name', 'password','password2','phoneNumber']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # validating password and confirm password while registration

    def validate(self, attrs):
        password= attrs.get('password')
        password2= attrs.get('password2')
        if password!= password2:
            raise serializers.ValidationError('Password and confirm password dose not matche..')

        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

# user login serializer

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225)
    class Meta:
        model= User
        fields=[ 'email','password']

# for all user 

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','email','name','phoneNumber']

#serializer for setting profile pic

# class UserProfilePicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UserProfilePic
#         fields=['profilePic']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['profilePic']

    def update( self, instance, validated_data):
        instance.profilePic= validated_data.get('profilePic',instance.profilePic)
        instance.save()
        return instance
    

class GetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','profilePic']