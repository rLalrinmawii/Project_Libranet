# Generated by Django 5.1 on 2024-10-29 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='availability',
            field=models.CharField(default=False),
        ),
    ]
