# Generated by Django 5.1.3 on 2024-12-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('user_inv_code', models.CharField(max_length=4, unique=True)),
                ('activated_inv_code', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
    ]