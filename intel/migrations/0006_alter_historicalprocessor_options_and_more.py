# Generated by Django 4.2.8 on 2023-12-17 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intel', '0005_historicalprocessor_hardware_shield_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalprocessor',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Intel processor', 'verbose_name_plural': 'historical Intel processors'},
        ),
        migrations.AlterModelOptions(
            name='processor',
            options={'ordering': ['product_id'], 'verbose_name': 'Intel processor', 'verbose_name_plural': 'Intel processors'},
        ),
        migrations.AlterModelTableComment(
            name='processor',
            table_comment='Intel processors and their specifications',
        ),
        migrations.AlterModelTable(
            name='processor',
            table='intel_processors',
        ),
    ]
