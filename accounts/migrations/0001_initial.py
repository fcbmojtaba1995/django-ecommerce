# Generated by Django 3.2.5 on 2021-08-01 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='username')),
                ('password', models.CharField(max_length=128, null=True, verbose_name='password')),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=300, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='phone')),
                ('national_code', models.CharField(blank=True, max_length=10, verbose_name='national code')),
                ('date_of_birth', models.DateField(null=True, verbose_name='date of birth')),
                ('is_set_password', models.BooleanField(default=False, verbose_name='is set password')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=6, verbose_name='code')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='code', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verify Code',
                'verbose_name_plural': 'Verify Codes',
                'db_table': 'verify_code',
            },
        ),
    ]
