# Generated by Django 5.1.5 on 2025-02-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0009_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
