# Generated by Django 4.2.5 on 2023-09-21 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_delete_customerorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordertransaction',
            name='total_amount',
        ),
    ]
