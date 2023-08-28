from rest_framework import serializers
from process.models import Capture

class CaptureSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Capture
        fields= ['captureImage', 'group','uploader']
