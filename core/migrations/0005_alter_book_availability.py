# Generated by Django 5.1 on 2024-11-01 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_book_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='availability',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
