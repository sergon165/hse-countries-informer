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


class WeatherSerializer(serializers.Serializer):
    """
    Сериализатор для данных о погоде.
    """

    temp = serializers.FloatField()
    pressure = serializers.IntegerField()
    humidity = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    description = serializers.CharField()


class CurrencySerializer(serializers.Serializer):
    """
    Сериализатор для данных о курсах валют.
    """

    base = serializers.CharField()
    date = serializers.DateField()
    rates = serializers.DictField()
