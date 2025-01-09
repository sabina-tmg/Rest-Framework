from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserBalance(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+", db_column='user_id')


    class Meta:
        managed = False
        db_table = 'balance'