# Generated by Django 3.2.5 on 2021-08-02 22:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=50, verbose_name='code')),
                ('valid_from', models.DateTimeField(verbose_name='valid from')),
                ('valid_to', models.DateTimeField(verbose_name='valid to')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='discount')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'db_table': 'coupon',
                'ordering': ('-created',),
            },
        ),
    ]