from django.db import models
import random

# Create your models here.
    
# Let's create models for user details and transfer money

class ThreeDigitAutoPrimaryKeyField(models.SmallAutoField):
    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

class User(models.Model):
    customerAccountNo = ThreeDigitAutoPrimaryKeyField()
    customerName = models.CharField(max_length=40)
    authCode = models.IntegerField(default=random.randint(100000, 999999))
    balance = models.FloatField()

    def __str__(self) -> str:
        return self.customerName
