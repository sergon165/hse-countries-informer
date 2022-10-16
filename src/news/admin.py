from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "title",
        "source",
        "published_at",
        "url",
    )

    search_fields = ("title", "description")

    list_filter = (
        "published_at",
        "created_at",
        "updated_at",
    )
