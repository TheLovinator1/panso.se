# Generated by Django 4.2.7 on 2023-12-10 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SitemapArticle',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap article',
                'verbose_name_plural': 'Sitemap articles',
                'db_table': 'webhallen_sitemap_article',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.article.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapCampaign',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap campaign',
                'verbose_name_plural': 'Sitemap campaigns',
                'db_table': 'webhallen_sitemap_campaign',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.campaign.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapCampaignList',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap campaign list',
                'verbose_name_plural': 'Sitemap campaign lists',
                'db_table': 'webhallen_sitemap_campaign_list',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.campaignList.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapCategory',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap category',
                'verbose_name_plural': 'Sitemap categories',
                'db_table': 'webhallen_sitemap_category',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.category.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapHome',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap home',
                'verbose_name_plural': 'Sitemap homes',
                'db_table': 'webhallen_sitemap_home',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.home.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapInfoPages',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap info page',
                'verbose_name_plural': 'Sitemap info pages',
                'db_table': 'webhallen_sitemap_info_pages',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.infoPages.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapManufacturer',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap manufacturer',
                'verbose_name_plural': 'Sitemap manufacturers',
                'db_table': 'webhallen_sitemap_manufacturer',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.manufacturer.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapProduct',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap product',
                'verbose_name_plural': 'Sitemap products',
                'db_table': 'webhallen_sitemap_product',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.product.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapRoot',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap root',
                'verbose_name_plural': 'Sitemap roots',
                'db_table': 'webhallen_sitemap_root',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='SitemapSection',
            fields=[
                ('loc', models.URLField(help_text='URL', primary_key=True, serialize=False)),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Sitemap section',
                'verbose_name_plural': 'Sitemap sections',
                'db_table': 'webhallen_sitemap_section',
                'db_table_comment': 'Table storing the https://www.webhallen.com/sitemap.section.xml sitemap',
            },
        ),
        migrations.CreateModel(
            name='WebhallenJSON',
            fields=[
                ('product_id', models.IntegerField(help_text='Product ID', primary_key=True, serialize=False)),
                ('product_json', models.JSONField(help_text='Product JSON')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
            ],
            options={
                'verbose_name': 'Webhallen JSON',
                'verbose_name_plural': 'Webhallen JSON Entries',
                'db_table': 'webhallen_json',
                'db_table_comment': 'Table storing JSON data from Webhallen API',
            },
        ),
        migrations.CreateModel(
            name='WebhallenSection',
            fields=[
                ('section_id', models.IntegerField(help_text='Section ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Updated')),
                ('meta_title', models.TextField(blank=True, help_text='Meta title', null=True)),
                ('active', models.BooleanField(help_text='Active', null=True)),
                ('icon', models.TextField(blank=True, help_text='Icon', null=True)),
                ('icon_url', models.URLField(blank=True, help_text='Icon URL', null=True)),
                ('name', models.TextField(blank=True, help_text='Name', null=True)),
                ('url', models.URLField(blank=True, help_text='URL', null=True)),
            ],
            options={
                'verbose_name': 'Webhallen section',
                'verbose_name_plural': 'Webhallen sections',
                'db_table': 'webhallen_section',
                'db_table_comment': 'Table storing Webhallen sections',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWebhallenSection',
            fields=[
                ('section_id', models.IntegerField(db_index=True, help_text='Section ID')),
                ('meta_title', models.TextField(blank=True, help_text='Meta title', null=True)),
                ('active', models.BooleanField(help_text='Active', null=True)),
                ('icon', models.TextField(blank=True, help_text='Icon', null=True)),
                ('icon_url', models.URLField(blank=True, help_text='Icon URL', null=True)),
                ('name', models.TextField(blank=True, help_text='Name', null=True)),
                ('url', models.URLField(blank=True, help_text='URL', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Webhallen section',
                'verbose_name_plural': 'historical Webhallen sections',
                'db_table': 'webhallen_section_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalWebhallenJSON',
            fields=[
                ('product_id', models.IntegerField(db_index=True, help_text='Product ID')),
                ('product_json', models.JSONField(help_text='Product JSON')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Webhallen JSON',
                'verbose_name_plural': 'historical Webhallen JSON Entries',
                'db_table': 'webhallen_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapSection',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap section',
                'verbose_name_plural': 'historical Sitemap sections',
                'db_table': 'webhallen_sitemap_section_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapRoot',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap root',
                'verbose_name_plural': 'historical Sitemap roots',
                'db_table': 'webhallen_sitemap_root_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapProduct',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap product',
                'verbose_name_plural': 'historical Sitemap products',
                'db_table': 'webhallen_sitemap_product_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapManufacturer',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap manufacturer',
                'verbose_name_plural': 'historical Sitemap manufacturers',
                'db_table': 'webhallen_sitemap_manufacturer_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapInfoPages',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap info page',
                'verbose_name_plural': 'historical Sitemap info pages',
                'db_table': 'webhallen_sitemap_info_pages_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapHome',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap home',
                'verbose_name_plural': 'historical Sitemap homes',
                'db_table': 'webhallen_sitemap_home_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapCategory',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap category',
                'verbose_name_plural': 'historical Sitemap categories',
                'db_table': 'webhallen_sitemap_category_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapCampaignList',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap campaign list',
                'verbose_name_plural': 'historical Sitemap campaign lists',
                'db_table': 'webhallen_sitemap_campaign_list_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapCampaign',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap campaign',
                'verbose_name_plural': 'historical Sitemap campaigns',
                'db_table': 'webhallen_sitemap_campaign_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSitemapArticle',
            fields=[
                ('loc', models.URLField(db_index=True, help_text='URL')),
                ('priority', models.FloatField(help_text='Priority', null=True)),
                ('active', models.BooleanField(help_text='If the URL is still in the sitemap', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sitemap article',
                'verbose_name_plural': 'historical Sitemap articles',
                'db_table': 'webhallen_sitemap_article_history',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
