# Generated by Django 4.0.4 on 2022-09-03 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qpass', '0009_alter_logs_options_customer_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='logos', to='qpass.customer', verbose_name='Ник посетителя'),
        ),
    ]
