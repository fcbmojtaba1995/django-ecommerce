from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login-register/', views.login_register_view, name='login_register'),
    path('login/confirm/<str:login_type>/<int:user_id>', views.login_confirm_view, name='login_confirm'),
    path('register/confirm/<int:user_id>', views.register_confirm_view, name='register_confirm'),
    path('profile/<int:user_id>', views.profile_view, name='profile'),
    path('profile/edit/personal-info/<int:user_id>', views.edit_profile_view, name='edit_profile'),
    path('profile/edit/password/<int:user_id>', views.edit_password_view, name='edit_password'),
    path('profile/edit/phone/<int:user_id>', views.edit_phone_view, name='edit_phone'),
    path('profile/edit/phone/verify/<int:user_id>/<str:new_phone>',
         views.edit_phone_verify_view, name='edit_phone_verify'),
    path('profile/edit/phone/verify/new-phone/<int:user_id>/<str:new_phone>',
         views.new_phone_verify_view, name='new_phone_verify'),
    path('profile/delete/<int:user_id>', views.delete_account_view, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),

]
