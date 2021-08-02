from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from suds.client import Client
from ecommerce.local_settings import ZARINPAL_MERCHANT_KEY, ZARINPAL_WEB_GATE_URL, \
    ZARINPAL_DESCRIPTION, ZARINPAL_CALLBACK_URL, ZARINPAL_START_PAY_URL
from .models import Order, OrderItem, Coupon
from .forms import CouponForm
from cart.cart import Cart


@login_required
def create_order_view(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
    return redirect('orders:order_detail', order.id)


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CouponForm()
    return render(request, 'orders/order_detail.html', {'order': order, 'form': form})


@require_POST
def apply_coupon_view(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, is_active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'This coupon dose not exist', 'danger')
            return redirect('orders:order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        messages.success(request, 'coupon is applied successfully', 'success')
        return redirect('orders:order_detail', order_id)


client = Client(ZARINPAL_WEB_GATE_URL)


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    amount = order.get_total_price()
    phone = request.user.phone
    email = request.user.email
    if email:
        result = client.service.PaymentRequest(
            ZARINPAL_MERCHANT_KEY, amount, ZARINPAL_DESCRIPTION, email, phone, ZARINPAL_CALLBACK_URL + str(order_id)
        )
    else:
        result = client.service.PaymentRequest(
            ZARINPAL_MERCHANT_KEY, amount, ZARINPAL_DESCRIPTION, phone, ZARINPAL_CALLBACK_URL + str(order_id)
        )

    if result.Status == 100:
        return redirect(ZARINPAL_START_PAY_URL + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required
def verify(request, order_id):
    if request.GET.get('Status') == 'OK':
        order = Order.objects.get(id=order_id)
        amount = order.get_total_price()
        result = client.service.PaymentVerification(ZARINPAL_MERCHANT_KEY, request.GET['Authority'], amount)
        if result.Status == 100:
            cart = Cart(request)
            cart.clear()
            order.paid = True
            order.save()
            messages.success(request, 'Transaction was successful', 'success')
            return redirect('shop:home')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted')
        else:
            return HttpResponse('Transaction failed.')
    else:
        return HttpResponse('Transaction failed or canceled by user')
