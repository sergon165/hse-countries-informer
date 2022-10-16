from rest_framework import serializers

from geo.models import Country, City


class CountrySerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных о стране.
    """

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "alpha2code",
            "alpha3code",
            "capital",
            "region",
            "subregion",
            "population",
            "latitude",
            "longitude",
            "demonym",
            "area",
            "numeric_code",
            "flag",
            "currencies",
            "languages",
        ]


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для данных о городе.
    """

    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "region",
            "latitude",
            "longitude",
            "country",
        ]
