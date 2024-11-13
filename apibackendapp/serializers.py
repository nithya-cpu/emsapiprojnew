from rest_framework import serializers #import module
from .models import Employee,Department
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    #ceating a custom field called group_name
    group_name = serializers.CharField(write_only=True,required=False )
    #write_only means the field will be used for input

    #function to create the user
    def create(self,validated_data):
        #we will recieve username,password and grp
        group_name=validated_data.pop("group_name",None)
        #as part of the secuirity ,encrypt the password and save it
        validated_data['password']=make_password(validated_data.get("password"))
        #create the user using the validated data  containing username and password.
        user =super(SignupSerializer,self).create(validated_data)
        #now we can zdd the created user to the group
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            #attempting create a group object with the specified group name
            user.groups.add(group) #add the user to that group
        return user #return the newly created user
    
    class Meta:
        model = User
        fields =['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #creating the custom fiels for username
    username=serializers.CharField()
    class Meta:
        model=User
        fields=['username','password']




#create serilalizer by inheriting Modelserilizer class
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:#will provide metadata to the model
        model = Department
        fields=('DepartmentId','DepartmentName')
        

#add function for employee name validation (should more than 3 chars)
def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("Name must be atleast 3 characters")
    return employee_name



#create serilalizer by inheriting Modelserilizer class
class EmployeeSerializer(serializers.ModelSerializer):
    #Department is acustom field in the serilizer
    #source ='DepartmentId says that the field should get data about the DepartmentId of the employee in the model
    Department = DepartmentSerializer(source='DepartmentId',read_only=True)
    #adding validation to EmployeeName
    #defining EmpoyeeName field as custom field so that we can add the validator
    EmployeeName=serializers.CharField(max_length=200,validators=[name_validation])
    class Meta:#will provide metadata to the model
        model = Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentId','Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:#will provide metadata to the model
        model = User
        fields=('id','username')#gets only this two field
        
    

    