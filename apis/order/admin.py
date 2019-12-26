from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from . import models


# Register your models here.

@admin.register(models.OrderInfo)
class OrderInfoAdmin(ImportExportModelAdmin):
    list_display = ['order_id', 'user', 'addr', 'pay_method', 'total_count', 'total_count', 'transit_price',
                    'order_status', 'trade_no']

    search_fields = list_display

    list_filter = list_display


@admin.register(models.OrderGoods)
class OrderGoodsAdmin(ImportExportModelAdmin):

    list_display = ['order', 'sku', 'count', 'price', 'comment']
    search_fields = list_display
    list_filter = list_display
