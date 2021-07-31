from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import LoginRegisterForm, VerifyForm, LoginByPasswordForm, EditProfileForm, \
    EditPasswordForm, SetPasswordForm, EditPhoneForm
from libs.utils import generate_username

User = get_user_model()


def login_register_view(request):
    if request.method == 'POST':
        next_url = request.POST.get("next", False)
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            phone_or_email = form.cleaned_data['phone_or_email']
            users = User.objects.filter(Q(email__iexact=phone_or_email) | Q(phone__exact=phone_or_email))
            if users.count() > 0:  # Login
                user = authenticate(username=users.first().username)

                if user is not None:

                    if user.is_set_password or not phone_or_email.startswith('0'):
                        return redirect('accounts:login_confirm', 'login-by-password', user.id)
                    else:
                        messages.success(request, 'SMS verification sent successfully', 'success')
                        return redirect('accounts:login_confirm', 'login-by-code', user.id)

                if next_url:
                    return redirect(next_url)

            else:  # Register
                if phone_or_email.startswith('0'):
                    user = User.objects.create_user(username=generate_username(), phone=phone_or_email)
                    messages.success(request, 'SMS verification sent successfully', 'success')
                    return redirect('accounts:register_confirm', user.id)

                else:
                    messages.error(request, 'your entered email not exists please enter your phone', 'danger')
                    return redirect('accounts:login_register')

    else:
        form = LoginRegisterForm()
    return render(request, 'accounts/login_register.html', context={'form': form})


def register_confirm_view(request, user_id):
    return verify_user_view(request, user_id, 'register')


def login_confirm_view(request, login_type, user_id):
    if login_type == 'login-by-code':
        return verify_user_view(request, user_id, 'login')
    elif login_type == 'login-by-password':
        return login_by_password_view(request, user_id)


def verify_user_view(user_request, user_id, redirect_status):
    form = VerifyForm(user_request.POST or None)
    if user_id:
        user = get_object_or_404(User, id=user_id)
        code = user.code
        if not user_request.POST:
            # send_verify_code(user.phone, str(code))
            print(code)

        if form.is_valid():
            if str(code) == form.cleaned_data['code']:
                code.save()
                user.is_verified = True
                user.save()
                login(user_request, user)
                messages.success(user_request, 'You logged in successfully', 'success')
                return redirect('accounts:login_register')
            else:
                messages.error(user_request, 'verify code is wrong please enter again', 'danger')
                if redirect_status == 'login':
                    return redirect('accounts:login_confirm', 'login-by-code', user_id)
                else:
                    return redirect('accounts:register_confirm', user_id)

    else:
        return HttpResponse('403 Forbidden')

    return render(user_request, 'accounts/verify.html', context={'form': form})


def login_by_password_view(request, user_id):
    form = LoginByPasswordForm(request.POST or None)
    if user_id:
        user = get_object_or_404(User, id=user_id)
        if form.is_valid():
            if user.check_password(form.cleaned_data['password']):
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('accounts:login_register')
            else:
                messages.error(request, 'password is wrong please enter again', 'danger')
                return redirect('accounts:login_confirm', 'login-by-password', user.id)

    return render(request, 'accounts/login_by_password.html', context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'you logged out successfully', 'success')
    return redirect('accounts:login_register')


@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/profile.html', context={'user': user})


@login_required
def edit_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user.first_name = cleaned_data['first_name']
            user.last_name = cleaned_data['last_name']
            user.email = cleaned_data['email']
            user.national_code = cleaned_data['national_code']
            user.date_of_birth = cleaned_data['date_of_birth']
            user.save()
            messages.success(request, 'your profile edited successfully', 'success')
            return redirect('accounts:profile', user_id)

    else:
        form = EditProfileForm(instance=user)
    return render(request, 'accounts/edit_profile.html', context={'form': form})


@login_required
def edit_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_set_password:
        edit_password_form = EditPasswordForm(request.POST or None)
        if edit_password_form.is_valid():
            current_password = edit_password_form.cleaned_data.get('current_password')
            new_password = edit_password_form.cleaned_data.get('new_password1')
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'your password changed successfully', 'success')
                return redirect('accounts:profile', user_id)
            else:
                messages.error(request, 'your current password is wrong', 'danger')
        return render(request, 'accounts/edit_password.html', context={'form': edit_password_form})
    else:
        set_password_form = SetPasswordForm(request.POST or None)
        if set_password_form.is_valid():
            password = set_password_form.cleaned_data.get('password1')
            user.set_password(password)
            user.is_set_password = True
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'your password set successfully', 'success')
            return redirect('accounts:profile', user_id)
        return render(request, 'accounts/edit_password.html', context={'form': set_password_form})


@login_required
def edit_phone_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditPhoneForm(request.POST)
        if form.is_valid():
            new_phone = form.cleaned_data.get('new_phone')
            if new_phone != user.phone:
                messages.success(request, 'SMS verification sent successfully', 'success')
                return redirect('accounts:edit_phone_verify', user_id, new_phone)
    else:
        form = EditPhoneForm(initial={'new_phone': user.phone})
    return render(request, 'accounts/edit_phone.html', context={'form': form})


@login_required
def edit_phone_verify_view(request, user_id, new_phone):
    form = VerifyForm(request.POST or None)
    if user_id:
        user = get_object_or_404(User, id=user_id)
        code = user.code
        if not request.POST:
            # send_verify_code(user.phone, str(code))
            print(code)

        if form.is_valid():
            if str(code) == form.cleaned_data['code']:
                code.save()
                messages.success(request, 'SMS verification sent for new phone successfully', 'success')
                return redirect('accounts:new_phone_verify', user_id, new_phone)
            else:
                messages.error(request, 'verify code is wrong please enter again', 'danger')

    else:
        return HttpResponse('403 Forbidden')

    return render(request, 'accounts/verify.html', context={'form': form})


@login_required
def new_phone_verify_view(request, user_id, new_phone):
    form = VerifyForm(request.POST or None)
    if user_id:
        user = get_object_or_404(User, id=user_id)
        code = user.code
        if not request.POST:
            # send_verify_code(user.phone, str(code))
            print(code)

        if form.is_valid():
            if str(code) == form.cleaned_data['code']:
                code.save()
                user.phone = new_phone
                user.save()
                messages.success(request, 'Your phone changed successfully', 'success')
                return redirect('accounts:profile', user_id)
            else:
                messages.error(request, 'verify code is wrong please enter again', 'danger')

    else:
        return HttpResponse('403 Forbidden')

    return render(request, 'accounts/verify.html', context={'form': form})


@login_required
def delete_account_view(request, user_id):
    if user_id == request.user.id:
        get_object_or_404(User, id=user_id).delete()
        messages.success(request, 'Your account has been deleted', 'success')
        return redirect('accounts:login_register')
    else:
        return redirect('accounts:login_register')
