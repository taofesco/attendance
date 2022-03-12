from django.shortcuts import render
import random
from datetime import datetime, timedelta


from django.http.response import JsonResponse
import time
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.generic import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

from account.models import *
from account.serializers import UserSerializer
from document.models import *
from document.serializers import *


class Login(APIView):
    def post(self, request, *args, **kwargs):
        cd = request.data
        user = authenticate(request,
                            username=cd['username'],
                            password=cd['password'])
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            employee = None
        if employee is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': str(user.username),
                })
            else:
                return Response({
                    "data": "Access Denied"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "data": "Wrong Username or Password"
            }, status=status.HTTP_400_BAD_REQUEST)


class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)



class GetAttendance(APIView):
    def get(self, request, card_id):
        employee = Employee.objects.get(card_id=card_id)
        try:
            attendance = Attendance.objects.get(employee=employee,date=date.today())
            if attendance.time_in:
                time_now = time.localtime()
                str_time = time.strftime('%H:%M', time_now)
                attendance.time_out = str_time
                attendance.save()
        except Attendance.DoesNotExist:
            time_now = time.localtime()
            str_time = time.strftime('%H:%M', time_now)
            attendance = Attendance.objects.create(
                employee=employee, date=date.today(), time_in=str_time)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

            

