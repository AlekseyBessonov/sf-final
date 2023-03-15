from rest_framework import serializers
from .models import Car, Maintains, Complaint


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('__all__')

class TOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintains
        fields = ('__all__')

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('__all__')