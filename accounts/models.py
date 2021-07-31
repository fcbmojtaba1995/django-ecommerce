from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import MyUserManager
from libs.utils import generate_verify_code


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'user'

    username = models.CharField(max_length=100, verbose_name='username', unique=True)
    password = models.CharField(_('password'), max_length=128, null=True)
    first_name = models.CharField(max_length=100, verbose_name='first name', blank=True)
    last_name = models.CharField(max_length=100, verbose_name='last name', blank=True)
    email = models.EmailField(max_length=300, verbose_name='email', blank=True)
    phone = models.CharField(max_length=12, verbose_name='phone', blank=True)
    national_code = models.CharField(max_length=10, verbose_name='national code', blank=True)
    date_of_birth = models.DateField(verbose_name='date of birth', null=True)
    is_set_password = models.BooleanField(default=False, verbose_name='is set password')
    is_verified = models.BooleanField(default=False, verbose_name='is verified')
    last_modified = models.DateTimeField(verbose_name='date modified', auto_now=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.phone:
            return self.phone
        else:
            return self.username


class VerifyCode(models.Model):
    code = models.CharField(max_length=6, verbose_name='code', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code')

    class Meta:
        verbose_name = 'Verify Code'
        verbose_name_plural = 'Verify Codes'
        db_table = 'verify_code'

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        verify_code = generate_verify_code()
        self.code = verify_code
        super().save(*args, **kwargs)
