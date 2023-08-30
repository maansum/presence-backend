from rest_framework import serializers
from alert.models import AlertModel


# serializers here

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model= AlertModel
        fields='__all__'


class GetAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model= AlertModel
        fields=['id','sender','send_at','read','group']