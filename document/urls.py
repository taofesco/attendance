
from django.urls import path, include
from django.conf.urls import handler404

from document.views import *


urlpatterns = [
    path('login/', Login.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),
    path('get_attendance/<card_id>/', GetAttendance.as_view()),
    path('attendance_list/', AttendanceList.as_view()),
    path('employee_list/', EmployeeList.as_view()),
]


