from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from libs.models import BaseModel
from shop.models import Product

User = get_user_model()


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    discount = models.IntegerField(
        verbose_name='discount', validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True, default=None
    )
    is_paid = models.BooleanField(default=False, verbose_name='is paid')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'order'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_price_after_apply_coupon(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField(verbose_name='price')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='quantity')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = 'order_item'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(BaseModel):
    code = models.CharField(max_length=50, verbose_name='code')
    valid_from = models.DateTimeField(verbose_name='valid from')
    valid_to = models.DateTimeField(verbose_name='valid to')
    discount = models.IntegerField(verbose_name='discount', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='is active')

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        db_table = 'coupon'
        ordering = ('-created',)

    def __str__(self):
        return self.code
