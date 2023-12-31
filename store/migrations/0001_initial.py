# Generated by Django 4.2.5 on 2023-09-20 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('contact', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='TimeStampedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-updated', '-created'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.timestampedmodel')),
                ('bar_code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('cost', models.FloatField()),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.image_directory_path)),
                ('on_display', models.BooleanField(default=True, verbose_name='this product is available?')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('store.timestampedmodel',),
        ),
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=120)),
                ('message', models.CharField(blank=True, max_length=120, null=True)),
                ('is_noted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('request_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=12, unique=True)),
                ('price', models.FloatField()),
                ('quantity', models.PositiveIntegerField()),
                ('total_amount', models.FloatField()),
                ('is_paid', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['-is_accepted', '-created'],
            },
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.timestampedmodel')),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.ordertransaction')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=('store.timestampedmodel',),
        ),
    ]
