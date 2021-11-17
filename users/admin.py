from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room as room_model


class RoomInline(admin.TabularInline):  # 8.6-2
    model = room_model

    filter_horizontal = (  # 2 참조 # 이렇게도 먹는다!!
        "amenities",
        "facilities",
        "house_rules",
    )


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (RoomInline,)  # 8.6-2

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    # list_display = UserAdmin.list_display + (
    #     "gender",
    #     "language",
    #     "currency",
    #     "superhost",
    # )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)


# 기존 장고 유저 모델을 이용할때.
# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):
#     """Custom User Admin"""

#     list_display = ("username", "email", "gender", "language", "currency", "superhost")
#     list_filter = ("language", "currency", "superhost")
