# Generated by Django 3.0 on 2024-01-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Levi', '0008_auto_20240107_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='favorite_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
