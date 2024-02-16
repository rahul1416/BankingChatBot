from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('customerAccountNo', 'customerName', 'authCode', 'balance')
admin.site.register(User,UserAdmin)
