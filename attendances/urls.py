from django.urls import path
from attendances.views import AttendanceView,AttendanceUpdateView

urlpatterns=[
    path('takeAttendance/',AttendanceView.as_view(), name='attendance taking'),
    path('updateAttendance/',AttendanceUpdateView.as_view(), name='attendance update'),


]