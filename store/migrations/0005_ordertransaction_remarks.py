# Generated by Django 4.2.5 on 2023-09-22 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_ordertransaction_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertransaction',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]