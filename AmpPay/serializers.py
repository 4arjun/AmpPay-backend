from rest_framework import serializers
from .models import EnergyUsage

class EnergyUsageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = EnergyUsage
        fields = ['username', 'datetime', 'usage_value', 'irms_current', 'irms_power', 'peak_power']

    def get_username(self, obj):
        username_mapping = self.context.get('username_mapping', {})
        return username_mapping.get(obj.user_id, '')
