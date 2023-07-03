from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from accounts.renderers import UserRanderer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserLoginSerializer, UserRegistrationSerializer, AllUserSerializer, ProfileSerializer,GetProfileSerializer
from accounts.models import User
from rest_framework.permissions import IsAuthenticated

# generating token mannually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        #'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes=[UserRanderer]
    def post(self, request, format= None):
        serializer= UserRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                { 'user':serializer.data,
                    'token':token,
                 
                    'message':"Registration successful"
                },
                status= status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)


# view for login
class UserLoginView(APIView):
    renderer_classes=[UserRanderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            email= serializer.data.get('email')
            password= serializer.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                userDetail= AllUserSerializer(user)


                return Response({
                    'user':userDetail.data,
                    'token':token,
                    'message':'Login successful '}, status= status.HTTP_200_OK)
            else:
                return Response({ 'message':'invalid email ', },
                                status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# to get all the register user
class AllUserView(APIView):
    def get(self,request, format= None):
        
        users = User.objects.all() #sab data haru row wise tancha
        serializer = AllUserSerializer(users, many=True)
        return Response({'users':serializer.data})
    






#for posting th profile of the user who  login
class ChangeProfilePicView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[FormParser,MultiPartParser]
    
    def post(self,request, format=None):
        user= request.user

        serializer= ProfileSerializer(instance=user, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user_id':user.id,'profile':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
#  to get the profile of the the login  user
class GetProfilePicView(APIView):
    permission_classes=[IsAuthenticated]
    

    def get(self,request, format=None):
        user= request.user
        users= User.objects.get(id=user.id)
        serializer= GetProfileSerializer(users)
        if serializer is not None:
            return Response( serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     