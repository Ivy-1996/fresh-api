from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings

from import_export.admin import ImportExportModelAdmin

from . import models


@admin.register(models.GoodsType)
class GoodsTypeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'logo', 'image_data']

    def image_data(self, attr):
        image_domain = getattr(settings, 'IMAGE_DOMAIN', None)
        if image_domain is None:
            resp = attr.image.url
        else:
            content = f'<img src="{image_domain + attr.image.url}" width=120>'
            resp = mark_safe(content)
        return resp


@admin.register(models.GoodsSKU)
class GoodsSKUAdmin(ImportExportModelAdmin):
    list_display = ['goods', 'name', 'desc', 'type', 'price', 'unite', 'image_data', 'stock', 'sales', 'status']

    search_fields = ['name', 'desc', 'price', 'unite', 'sales']

    list_filter = ['goods'] + search_fields

    def image_data(self, attr):
        image_domain = getattr(settings, 'IMAGE_DOMAIN', None)
        if image_domain is None:
            resp = attr.image.url
        else:
            content = f'<img src="{image_domain + attr.image.url}" width=40>'
            resp = mark_safe(content)
        return resp

    image_data.short_description = '商品图片'
