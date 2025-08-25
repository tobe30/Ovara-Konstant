from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource
from dashboard.models import Product, Purchase, Sale, Type,Notification, BC, Number8, Ds9c, Np7a, Customer, BCPurchase, BCSale, NPurchase, NSale, DsPurchase, DSSale, N7Purchase
# Register your models here.

class ProductAdmin(ImportExportModelAdmin):
    pass

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ('item_id', 'name', 'type', 'cost_per_unit', 'current_stock', 'total_sold','total_cost_value')

class BCAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'type', 'unit', 'current_stock', 'total_sold','total_cost_value')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase_date', 'price', 'unit_purchased', 'point_of_contact')
    
class BCPurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase_date', 'price', 'unit_purchased', 'point_of_contact')
    
class NPurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase_date', 'price', 'unit_purchased', 'point_of_contact')
    
class DsPurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase_date', 'price', 'unit_purchased', 'point_of_contact')
    
class N7PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'purchase_date', 'price', 'unit_purchased', 'point_of_contact')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sales_date', 'price', 'unit_sold', 'point_of_contact')  

class BCSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sales_date', 'price', 'unit_sold', 'point_of_contact')  

class NSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sales_date', 'price', 'unit_sold', 'point_of_contact') 
    
class DSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sales_date', 'price', 'unit_sold', 'point_of_contact')   
    
admin.site.register(BC, BCAdmin)
admin.site.register(BCSale, BCSaleAdmin)
admin.site.register(NSale, NSaleAdmin)
admin.site.register(DSSale, DSaleAdmin)



admin.site.register(BCPurchase, BCPurchaseAdmin)
admin.site.register(NPurchase, NPurchaseAdmin)
admin.site.register(DsPurchase, DsPurchaseAdmin)
admin.site.register(N7Purchase, N7PurchaseAdmin)

admin.site.register(Number8)
admin.site.register(Ds9c)
admin.site.register(Np7a)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Type)  # Registering the Type model
admin.site.register(Notification)
admin.site.register(Customer)