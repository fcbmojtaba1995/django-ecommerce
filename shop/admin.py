from django.contrib import admin

from .models import Category, Product, ProductImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub_category', 'slug', 'created')
    prepopulated_fields = {'slug': ('name',)}


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created')
    list_filter = ('available', 'created')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    actions = ('make_available',)
    inlines = (ProductImagesInline,)

    def make_available(self, request, queryset):
        rows = queryset.update(available=True)
        self.message_user(request, f'{rows} rows updated')

    make_available.short_description = 'Make available'


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product',)
