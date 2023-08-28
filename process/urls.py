from django.urls import path
from process.views import CaptureView


urlpatterns=[
    path('photo/',CaptureView.as_view(),name='capture_view')
]