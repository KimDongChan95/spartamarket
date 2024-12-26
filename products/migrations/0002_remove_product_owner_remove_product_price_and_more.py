# Generated by Django 5.1.4 on 2024-12-26 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.AddField(
            model_name="product",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True, related_name="liked_products", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
