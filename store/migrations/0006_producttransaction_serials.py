# Generated by Django 4.2.5 on 2023-10-04 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_ordertransaction_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttransaction',
            name='serials',
            field=models.TextField(blank=True, null=True),
        ),
    ]
