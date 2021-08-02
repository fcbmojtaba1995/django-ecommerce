from django.db import models
from django.urls import reverse
from libs.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=200, verbose_name='name')
    slug = models.SlugField(max_length=300, verbose_name='slug')
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True
    )
    is_sub_category = models.BooleanField(default=False, verbose_name='is sub category')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_filter', args=[self.id, self.slug])


class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200, verbose_name='name')
    slug = models.SlugField(max_length=300, verbose_name='slug', unique=True)
    description = models.TextField(verbose_name='description')
    price = models.IntegerField(verbose_name='price')
    available = models.BooleanField(default=True, verbose_name='available')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/%Y/%m/%d', verbose_name='image')

    class Meta:
        verbose_name = 'Product Images'
        verbose_name_plural = 'Product Images'
        db_table = 'product_images'

    def __str__(self):
        return self.product.name
