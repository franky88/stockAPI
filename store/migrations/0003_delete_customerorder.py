# Generated by Django 4.2.5 on 2023-09-20 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_delete_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerOrder',
        ),
    ]
