from django.contrib import admin
from .models import Product, Category, Order, OrderDetail, Cart


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock', 'category_id', 'created_at', 'updated_at')
    list_filter = ('category_id',)
    search_fields = ('name', 'description')
    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    ordering = ('id',)
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'total_price', 'created_at', 'updated_at')
    list_filter = ('user_id', 'created_at')
    search_fields = ('user_id__username', 'user_id__email')
    ordering = ('-created_at',)


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_id', 'quantity', 'price', 'created_at', 'updated_at')
    list_filter = ('order_id', 'product_id')
    search_fields = ('order_id__id', 'product_id__name')
    ordering = ('order_id',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'quantity', 'created_at', 'updated_at')
    list_display_links = ('user_id', 'product_id')
    list_filter = ('user_id', 'product_id')
    search_fields = ('user_id__username', 'product_id__name')
    ordering = ('user_id',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Cart, CartAdmin)
