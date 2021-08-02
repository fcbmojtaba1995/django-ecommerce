from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<int:category_id>/<slug:slug>', views.home_view, name='category_filter'),
    path('product/detail/<slug:slug>/', views.product_detail_view, name='product_detail'),
]
