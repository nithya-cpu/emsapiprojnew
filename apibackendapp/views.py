from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee,Department
from django.contrib.auth.models import User
from .serializers import EmployeeSerializer,DepartmentSerializer,UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.

#create an API view for signup
class SignupAPIView(APIView):
    permission_classes = [AllowAny] #signup doesnot need logging in
    #defining post function to handle signup post data
    def post(self,request):
        #create an object for signupSerilizer
        #by giving the data recieved to its constructor
        serializer=SignupSerializer(data = request.data)
        if serializer.is_valid():
            #create a new user if the serializer is valid
            user=serializer.save() #will give baack a user object
            #after craeting the user,create a token for the user
            token,created=Token.objects.get_or_create(user=user) #will give back  token object
            #once user is created,give back the responsewith userid,username,token,group
            return Response({
                "user_id":user.id,
                "username":user.username,
                "token":token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
                #give back the first role back id of the user if the rolr/group exists
            },status=status.HTTP_201_CREATED)
        else:
            #if serializer is not valid
            response = {'status':status.HTTP_400_BAD_REQUEST, 'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        

#create an API view for Login
class LoginAPIView(APIView):
    permission_classes = [AllowAny] #login doesnot need logging in
    #defining post function to handle login post data
    def post(self,request):
        #create an object for signupSerilizer
        #by giving the data recieved to its constructor
        serializer=LoginSerializer(data = request.data)
        if serializer.is_valid():
            #get the username,passwordfrom the validated data
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            #try to authenticate the user using this username and password
            #if successfully authenticated,it will return back a valid user object
            user=authenticate(request,username=username,password=password)
            if user is not None:
                #get the token for the authenticated user
                token =Token.objects.get(user=user)
                response= {
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token":token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)#login was success
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid username or password",
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)#login failed
        else:
            #if serializer is not valid
            response = {'status':status.HTTP_400_BAD_REQUEST, 'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)






#create view set class inheriting the ModelViewset class
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()#get all objects of model
    serializer_class= DepartmentSerializer#and rend it using serlizer
    #permission_classes = [] # to bypass the authentication
    permission_classes = [IsAuthenticated] # to restrict for login users


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()#get all objects of model
    serializer_class= EmployeeSerializer#and rend it using serlizer
    #add search option usinh employee name or designation
    filter_backends = [filters.SearchFilter]#create a search filter
    search_fields=['EmployeeName','Designation']#add the fields to search
    permission_classes = [] # to bypass the authentication
    #permission_classes = [IsAuthenticated] # to restrict for login users


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()#get all objects of model
    serializer_class= UserSerializer#and rend it using serlizer
    #permission_classes = [] # to bypass the authentication
    permission_classes = [IsAuthenticated] # to restrict for login users
    
