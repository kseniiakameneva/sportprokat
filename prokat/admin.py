from django.contrib import admin
from prokat.models import Category, Product, Type, Order


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Type)
admin.site.register(Order)

'''''''''
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'phone', 'date', 'date_end', 'stat')

    class Meta:
        model = Order


admin.site.register(Order,OrderAdmin)
'''''