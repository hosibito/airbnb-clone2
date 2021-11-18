from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]


"""
# 11 100%수동이나 함수형일때
urlpatterns = [path("", room_views.all_rooms, name="home")]
"""
