from django.urls import path

from news.views import get_news

urlpatterns = [
    path("<str:alpha2code>", get_news, name="news"),
]
