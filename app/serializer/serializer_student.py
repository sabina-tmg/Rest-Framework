from rest_framework import serializers
from app.models import Student
import re

def global_mobile_number(mobile_number):
    if not re.match(r'^\d{10}$', mobile_number):
        raise serializers.ValidationError("Mobile Number must be exactly 10 digits.")
    if Student.objects.filter(mobile_number=mobile_number).exists():
        raise serializers.ValidationError("Mobile Number already exists!")

class StudentSerializers(serializers.Serializer):
    studentName = serializers.CharField(
        source='name', 
        error_messages={"blank": "Name cannot be blank!"}
    )
    studentAddress = serializers.CharField(
        source='address', 
        error_messages={"blank": "Address cannot be blank!"}
    )
    studentAge = serializers.IntegerField(
        source='age', 
        error_messages={"blank": "Age cannot be blank!"}
    )
    mobileNumber = serializers.CharField(
        source='mobile_number', 
        validators=[global_mobile_number], 
        error_messages={"blank": "Mobile Number cannot be blank!"}
    )
    rollNumber = serializers.IntegerField(
        source='roll_number', 
        error_messages={"blank": "Roll Number cannot be blank!"}
    )
    reference_id = serializers.ReadOnlyField()

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
     instance.name = validated_data.get('name', instance.name)
     instance.address = validated_data.get('address', instance.address)
     instance.age = validated_data.get('age', instance.age)
     instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
     instance.roll_number = validated_data.get('roll_number', instance.roll_number)
    # Save the updated instance
     instance.save()
     return instance
    
    def validate_studentAge(self, age):
        if age < 0 or age > 100:
            raise serializers.ValidationError(f"Invalid age: {age}. Age must be between 0 and 100.")
        return age
    
    def validate_mobile_number(self, mobile_number):
    # Check if the mobile number is exactly 10 digits
        if not re.match(r'^\d{10}$', mobile_number):
          raise serializers.ValidationError("Mobile Number must be exactly 10 digits.")
    
    # Check if the mobile number already exists in the database
        if self.instance:
        # Exclude the current instance while checking for duplicates
           if Student.objects.filter(mobile_number=mobile_number).exclude(id=self.instance.id).exists():
             raise serializers.ValidationError("Mobile Number already exists!")
        else:
        # Check for duplicates without excluding any instance
          if Student.objects.filter(mobile_number=mobile_number).exists():
            raise serializers.ValidationError("Mobile Number already exists!")
        return mobile_number


    def validate_rollNumber(self, roll_number):
        if roll_number <= 0:
            raise serializers.ValidationError("Roll Number must be a positive integer.")
        return roll_number
