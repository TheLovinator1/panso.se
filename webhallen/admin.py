from __future__ import annotations

from django.contrib import admin

from .models import (
    SitemapArticle,
    SitemapCampaign,
    SitemapCategory,
    SitemapHome,
    SitemapInfoPages,
    SitemapManufacturer,
    SitemapProduct,
    SitemapSection,
    WebhallenProductJSON,
)

admin.site.register(SitemapArticle)
admin.site.register(SitemapCampaign)
admin.site.register(SitemapCategory)
admin.site.register(SitemapHome)
admin.site.register(SitemapInfoPages)
admin.site.register(SitemapManufacturer)
admin.site.register(SitemapProduct)
admin.site.register(SitemapSection)
admin.site.register(WebhallenProductJSON)
