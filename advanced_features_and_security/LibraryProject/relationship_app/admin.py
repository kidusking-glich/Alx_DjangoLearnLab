from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


class CustomeUserAdmin(UserAdmin):

    fieldsets =UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

admin.site.register(CustomUser, CustomeUserAdmin)