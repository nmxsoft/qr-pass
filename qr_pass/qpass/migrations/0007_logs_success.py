# Generated by Django 4.0.4 on 2022-05-17 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qpass', '0006_alter_logs_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='success',
            field=models.BooleanField(default=False, verbose_name='Попытка входа'),
        ),
    ]