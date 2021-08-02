from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.create_order_view, name='create_order'),
    path('detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('apply/<int:order_id>/', views.apply_coupon_view, name='apply_coupon'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('verify/<int:order_id>/', views.verify, name='verify'),
]
