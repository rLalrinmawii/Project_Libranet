# Generated by Django 5.1 on 2024-11-06 14:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cartitem_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='embedding',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
    ]
