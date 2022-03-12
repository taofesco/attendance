from rest_framework import serializers
from document.models import *
from django.contrib.auth.password_validation import validate_password


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    employee_firstname = serializers.CharField(
        source="employee.first_name", read_only=True)
    employee_lastname = serializers.CharField(
        source="employee.last_name", read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
