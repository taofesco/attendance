from django.contrib import admin
from document.models import *

# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', )
    search_fields = ('first_name',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee','date', 'time_in', 'time_out')
    search_fields = ('employee',)
