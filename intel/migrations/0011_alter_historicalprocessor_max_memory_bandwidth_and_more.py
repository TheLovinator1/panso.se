# Generated by Django 4.2.8 on 2023-12-17 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0010_historicalprocessor_digital_thermal_sensor_temperature_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprocessor',
            name='max_memory_bandwidth',
            field=models.BigIntegerField(blank=True, help_text='The maximum memory bandwidth the processor supports. In bytes per second.', null=True, verbose_name='Max Memory Bandwidth'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='max_memory_bandwidth',
            field=models.BigIntegerField(blank=True, help_text='The maximum memory bandwidth the processor supports. In bytes per second.', null=True, verbose_name='Max Memory Bandwidth'),
        ),
    ]
