from rest_framework import serializers
from .models import StoreStatus, Timing, Timezone, Report

class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreStatus
        fields = '__all__'

class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = '__all__'

class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'