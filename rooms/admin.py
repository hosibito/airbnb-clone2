from django.contrib import admin

from django.utils.html import mark_safe

from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "create", "update", "used_by")

    def used_by(self, obj):
        return obj.room_set.count()


class PhotoInline(admin.TabularInline):  # 노트 8.6 -2 참조 (어드민 내부에 다른 어드민을 추가한다.)

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "city", "price")},
        ),
        (
            "Time",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 목록 숨김 그외에 여러기능들이 있다.
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host", "room_type")},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # 2 manytomanyfield 는 list_display에 표시할수 없으므로 함수로 만들어 표시한다.
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price")

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)  # 노트 8.6 참조 ( 외부검색해서 선택이 되도록한다. )

    inlines = (PhotoInline,)  # 노트 8.6 -2 참조

    search_fields = ("=city", "^host__username")  # 6.1

    filter_horizontal = (  # 6.2 참조
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):  # 노트 #7 볼것.  3 첫번째인자 : 현 클래스 자체 두번째 인자 : 표시될 현제 row
        # print(obj)  # 집입니다요
        # print(obj.amenities)  # rooms.Amenity.None
        # print(obj.amenities.all())  # <QuerySet [<Amenity: Washer>]>
        # print(obj.amenities.count())  # 1
        return obj.amenities.count()

    count_amenities.short_description = "시설들!!"

    def count_photos(self, obj):  # Room model에 photo가 없다!
        # print(obj.photo_set.count())  # 노트 #7 볼것.. Django ORM!!!!
        return obj.photo_set.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):  # 노트 8.5참조
        # print(obj.file) # room_photos/3612017.jpeg
        # print(dir(obj.file)) # 이것저것 많음..
        # print(type(obj.file)) # <class 'django.db.models.fields.files.ImageFielsFile'>
        # print(obj.file.path) # 파일 경로가 나옴
        # print(obj.file.url) # url 경로가 나옴
        # print(obj.file.height) # 사진의 높이
        # print(obj.file.width) # 사진의 폭
        # print(obj.file.size) # 사이즈

        return mark_safe(f"<img height='70px' src='{obj.file.url}' />")

    get_thumbnail.short_description = "썸네일"


"""   6.1
    여러 검색방법이 있다. "^city",  "=city" 등등
    "host__username" self.host.username 를 검색헤서 사용한다.

    상단 검색창을 만들어준다. 
"""


"""    6.1
    ManyToManyField 에서만 작동한다.
    어드민 에서
    샤워
    wifi     +
    washer

    부분을  검색과 선택이 되는 화면으로 바꿔준다.
"""
