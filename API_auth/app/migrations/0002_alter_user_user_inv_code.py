# Generated by Django 5.1.3 on 2024-12-02 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_inv_code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
