from rest_framework import serializers

from geo.serializers import CountrySerializer
from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных о новости.
    """

    country = CountrySerializer(read_only=True)

    class Meta:
        model = News
        fields = [
            "country",
            "source",
            "author",
            "title",
            "description",
            "url",
            "published_at",
        ]
        ordering = ("published_at",)
