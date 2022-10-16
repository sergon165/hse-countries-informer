from django.contrib import admin

from geo.models import Country, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "alpha2code",
        "alpha3code",
        "numeric_code",
        "area",
        "population",
        "created_at",
        "updated_at",
    )

    search_fields = ("name", "alpha3code", "numeric_code")

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "region",
        "created_at",
        "updated_at",
    )

    search_fields = ("name", "region")

    list_filter = (
        "created_at",
        "updated_at",
    )
