from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Product(models.Model):
    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='', null=True, blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = '注文'
        verbose_name_plural = '注文'

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"注文ID:{self.id}"


class OrderDetail(models.Model):
    class Meta:
        db_table = 'order_details'
        verbose_name = '注文詳細'
        verbose_name_plural = '注文詳細'

    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    class Meta:
        db_table = 'carts'
        verbose_name = 'カート'
        verbose_name_plural = 'カート'

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
