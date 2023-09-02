from rest_framework import serializers
from alert.models import AlertModel


# serializers here

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model= AlertModel
        fields='__all__'


class GetAlertSerializer(serializers.ModelSerializer):
    groupname = serializers.SerializerMethodField()
    sendername = serializers.SerializerMethodField()

    class Meta:
        model = AlertModel
        fields = ['id', 'message', 'sender', 'send_at', 'read', 'group', 'groupname', 'sendername']

    def get_groupname(self, obj):
        # Replace this with your logic to compute groupname
        if obj.group:
            return obj.group.name  # Assuming 'name' is a field in your GroupModel
        return None

    def get_sendername(self, obj):
        # Replace this with your logic to compute sendername
        if obj.sender:
            return obj.sender.name  # Assuming 'name' is a field in your SenderModel
        return None
