from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from shop.forms import AddToCartForm
from .forms import RemoveFormCartForm


def cart_detail_view(request):
    cart = Cart(request)
    form = RemoveFormCartForm()
    return render(request, 'cart/cart_detail.html', context={'cart': cart, 'form': form})


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart.add(product=product, quantity=quantity)
    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = RemoveFormCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart.remove(product=product, quantity=quantity)
    return redirect('cart:cart_detail')
