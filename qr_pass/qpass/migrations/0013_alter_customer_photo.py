# Generated by Django 4.0.4 on 2022-09-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qpass', '0012_alter_customer_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photo/', verbose_name='Фото'),
        ),
    ]
