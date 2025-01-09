from django.db import models
import uuid
from django.contrib.auth.models import User


def uuid_generate():
    return uuid.uuid4().hex
class BaseModel(models.Model):
    reference_id = models.CharField(max_length=32, unique=True, default=uuid_generate)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_column="created_by", null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, db_column="updated_by", null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Student(BaseModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    roll_number = models.IntegerField(null=True, unique=True)

    class Meta:
        db_table = "student"
        managed=False

class Course(BaseModel):
    name = models.CharField(max_length=100)
    pub_date = models.DateField(null=True)
    page = models.IntegerField()

    class Meta:
        db_table = 'course'
