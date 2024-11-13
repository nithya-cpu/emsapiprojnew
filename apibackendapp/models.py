from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

# Create your models here.
#create a reciever for the signal 'post_save' for the user model
#once it is created create a token for that user
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)#create token for user





#creating a department model class by inheriting the model class
class Department(models.Model):
    DepartmentId= models.AutoField(primary_key=True)
    DepartmentName=models.CharField(max_length=200)
    #instead of the memory address of the object,
    #we need to return the name of the department
    def __str__(self):
        return self.DepartmentName
    

class Employee(models.Model):
    EmployeeId= models.AutoField(primary_key=True)
    EmployeeName=models.CharField(max_length=200)
    Designation=models.CharField(max_length=150)
    DateOfJoining=models.DateField()
    #depid is a foriegn key of the department model
    #when a department is deleted all the employees under will be deleted
    DepartmentId=models.ForeignKey(Department,on_delete=models.CASCADE)
    Contact=models.CharField(max_length=150)
    IsActive=models.BooleanField(default=True)

    
    def __str__(self):
        return self.EmployeeName
    
