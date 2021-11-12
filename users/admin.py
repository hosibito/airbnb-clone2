from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

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
