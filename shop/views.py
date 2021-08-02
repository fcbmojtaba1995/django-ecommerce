from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .forms import AddToCartForm

def home_view(request, category_id=None, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_sub_category=False)
    if category_id and slug:
        category = get_object_or_404(Category, id=category_id, slug=slug)
        products = products.filter(category=category)
    return render(request, 'shop/products.html', context={'products': products, 'categories': categories})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = product.category.all()
    form = AddToCartForm()
    return render(
        request, 'shop/product_detail.html',
        context={'product': product, 'categories': categories, 'form': form}
    )
