from django.contrib import admin

from .models import Customer, Logs, Device


@admin.register(Customer)
class PassRegister(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'real_name',
        'access',
        'key',
        'master'
    )


@admin.register(Logs)
class LogsRegister(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'visit',
        'success',
    )


@admin.register(Device)
class DeviceRegister(admin.ModelAdmin):
    list_display = (
        'id',
        'dev_id',
        'create_time'
    )
