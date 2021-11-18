from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]


""" note # 12 함수형 detailvoew(404관련포함)
urlpatterns = [path("<int:pk>/", views.room_detail, name="detail")]
"""
