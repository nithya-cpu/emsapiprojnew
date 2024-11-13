from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from .models import Department,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer
from rest_framework import status

# Create your tests here.
#creating new emloyeeViewSet class inheriting the APITestCase class
class EmployeeViewSetTest(APITestCase):
    #defining a function to setup some basic data for testing
    def setUp(self):
        #create a sample department
        self.department = Department.objects.create(DepartmentName="HR")
        #creating a sample employee object and assigning the department
        self.employee = Employee.objects.create(
            EmployeeName="Jackie Chan",
            Designation="Kungfu Master",
            DateOfJoining = date(2024, 11, 13),
            DepartmentId= self.department,
            Contact="china",
            IsActive =True
        )
        #since we are testing Api ,we need to create an APIClient object
        self.client=APIClient()

    #defining functions to test employee listing api/endpoint
    def test_employee_list(self):
        #the default reverse url for listing modelname-list
        url = reverse('employee-list')
        response = self.client.get(url) #send the a[i url and get the response get all the employee objects
        employees = Employee.objects.all()
        #create a serilalizer object from EmployeeSerializer
        serializer = EmployeeSerializer(employees,many=True)#get all employees

        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data,serializer.data)
        #check if serializer data matches the actual data format

    #TEST CASE 2:To get a particular employee details
    #defining function to test employee listing api/endpoint
    def test_employee_details(self):
        #the default reverse url for listing modelname-list
        #also provide the employee id as argument
        url = reverse('employee-details',args=[self.employee.EmployeeId])
        response = self.client.get(url) #send the api url and get the response get all the employee objects
       
        #create a serilalizer object from EmployeeSerializer using the setup data
        serializer = EmployeeSerializer(self.employee)#get all employees

        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data,serializer.data)
        #check if serializer data matches the actual data format


