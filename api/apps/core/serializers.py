from rest_framework import serializers
from .models import CoreModel

class CoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreModel
        fields = ['id', 'name', 'description', 'created_at']
