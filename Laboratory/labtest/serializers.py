from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    
    def validate_value(self,value):
        if value < 0:
            raise serializers.ValidationError("Value cannot be negative")
        return value

class TestSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['test_name','value','unit','test_date','is_abnormal'] 

# class StatsSerialiser(serializers.Serializer):
#     min_value = serializers.FloatField()
#     max_value = serializers.FloatField()
#     avg_value = serializers.FloatField()
#     total_test = serializers.IntegerField()
#     abnormal_count= serializers.IntegerField()

