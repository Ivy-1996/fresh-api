from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models


# Register your models here.

@admin.register(models.Address)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'receiver', 'addr', 'zip_code', 'phone', 'is_default']
