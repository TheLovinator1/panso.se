# Generated by Django 4.2.8 on 2023-12-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0009_alter_historicalprocessor_base_frequency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprocessor',
            name='digital_thermal_sensor_temperature_max',
            field=models.FloatField(blank=True, help_text='Digital Thermal Sensor (DTS) max temperature. In celsius.', null=True, verbose_name='Digital Thermal Sensor (DTS) max temperature'),
        ),
        migrations.AddField(
            model_name='processor',
            name='digital_thermal_sensor_temperature_max',
            field=models.FloatField(blank=True, help_text='Digital Thermal Sensor (DTS) max temperature. In celsius.', null=True, verbose_name='Digital Thermal Sensor (DTS) max temperature'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='operating_temperature_max',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The maximum operating temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Operating Temperature Max'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='operating_temperature_min',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The minimum operating temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Operating Temperature Min'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='t_case',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The maximum temperature allowed at the processor Integrated Heat Spreader (IHS).', max_digits=5, null=True, verbose_name='T Case'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='t_junction',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The highest temperature the processor can reach without damaging it. In celsius.', max_digits=5, null=True, verbose_name='T Junction'),
        ),
        migrations.AlterField(
            model_name='historicalprocessor',
            name='thermal_velocity_boost_temperature',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The thermal velocity boost temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Thermal Velocity Boost Temperature'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='operating_temperature_max',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The maximum operating temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Operating Temperature Max'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='operating_temperature_min',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The minimum operating temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Operating Temperature Min'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='t_case',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The maximum temperature allowed at the processor Integrated Heat Spreader (IHS).', max_digits=5, null=True, verbose_name='T Case'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='t_junction',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The highest temperature the processor can reach without damaging it. In celsius.', max_digits=5, null=True, verbose_name='T Junction'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='thermal_velocity_boost_temperature',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The thermal velocity boost temperature of the processor. In celsius.', max_digits=5, null=True, verbose_name='Thermal Velocity Boost Temperature'),
        ),
    ]
