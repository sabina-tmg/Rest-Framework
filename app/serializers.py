from rest_framework import serializers
from.models import Student

class TestSerializers(serializers.Serializer):
    name = serializers.CharField(error_messages={"blank": "Name cannot be blank."})
    address=serializers.CharField(error_messages={"blank": "Address cannot be blank."})
    age=serializers.IntegerField(error_messages={"blank": "Name cannot be blank."})
    mobile_number=serializers.CharField(error_messages={"blank": "Mobile_number cannot be blank."})

    def create(self, validated_data):
        return Student.objects.create(**validated_data)  
    
    def update(self, instance, validated_data):
        validated_data={"name":"sabina", "address":"ktm"}
        instance.name = validated_data.get('name', instance.name)


    def validate_age(self,age):
        if age>100 or age<0:
            raise serializers.ValidationError("age  must be valid in 1 to 100 in range")
        return age
    
    def validate_mobile_number(self,value):
        if Student.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number is already exists")
        return value