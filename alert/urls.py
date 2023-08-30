from django.urls import path 
from alert.views import AlertView,AlertDetailView

urlpatterns=[
    path('getnotification/',AlertView.as_view(),name='get_notification'),
    path('sendnotification/',AlertView.as_view(),name='send_notification'),
    path('accknotification/<int:pk>',AlertDetailView.as_view(),name='acck_notification'),


]