from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("search/", views.SearchView.as_view(), name="search"),
]


""" note # 12 함수형 detailvoew(404관련포함)
urlpatterns = [path("<int:pk>/", views.room_detail, name="detail")]
"""

"""
path("search/", views.search, name="search"),
"""
