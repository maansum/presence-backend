from django.urls import path
from attendances.views import AttendanceView,AttendanceUpdateView,GetAttendanceView,PictureView,MyAttendanceReportView,AttendanceGroupView

urlpatterns=[
    path('takeAttendance/',AttendanceView.as_view(), name='attendance taking'),
    path('updateAttendance/',AttendanceUpdateView.as_view(), name='attendance update'),
    path('getAttendance/',GetAttendanceView.as_view(), name='attendance getting'),
    path('pictures/',PictureView.as_view(), name='pictures'),
    path('reports/my/',MyAttendanceReportView.as_view(), name='my reports'),
    path('reports/myGroups/',AttendanceGroupView.as_view(), name='my reports'),





    
]