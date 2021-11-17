from django.db import models
from django_countries.fields import CountryField

from core import models as core_models

# from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):  # 노트 4 or 하단 참조

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name", "create"]
        #  ordering = ["name", "-create"]

    # Entire place, Private room, Hotel room, Shared room 등의 옵션이 올곳


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name = "시설"
        verbose_name_plural = "시설들"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")  # 8.3
    # room = models.ForeignKey(Room, on_delete=models.CASCADE) Room 정의가 밑에있어서 에러
    room = models.ForeignKey("Room", on_delete=models.CASCADE)  # 4.2 또는 하단설명 참조

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()  # 노트 4.1 참조
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    # room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    # amenities = models.ManyToManyField(Amenity)
    # facilities = models.ManyToManyField(Facility)
    # house_rules = models.ManyToManyField(HouseRule)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    house_rules = models.ManyToManyField("HouseRule", blank=True)
    # host = models.ForeignKey(
    #     "users.User", related_name="rooms", on_delete=models.CASCADE
    # )
    # room_type = models.ForeignKey(
    #     "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    # )
    # amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    # facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    # house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):  # 8.0 참조
        all_reviews = self.review_set.all()
        all_rating = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # print(review.rating_average())
                all_rating += review.rating_average()  # reviews/model 에 있으므로 사용가능.
            return round(all_rating / len(all_reviews), 2)
        return 0


"""  노트 4.1 참조
    https://github.com/SmileyChris/django-countries
    나라이름을 입력할수 있게 해준다.

    pip install django-countries
    Add "django_countries" to INSTALLED_APPS
    from django_countries.fields import CountryField
"""

""" 노트 4 참조
    모델에 초이스를 사용해서 직접 박아넣을수도 있다.
    어찌보면 따로 만들고 어드민에서 추가안해줘도 되니 편할수도 있다.
    다만 저건 프로그래머의 방법이다. 프로그래머가 아닌 누군가도 추가할수 있으려면
    이렇게 만드는게 낫다. 협업시에도 유리하다.
"""

""" 4.2
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Room 정의가 밑에있어서 에러 따라서
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    "Room" 으로 string 로 바꿔주면 된다. ( model class명)


    string를 이용하면 임포트도 필요없어 지는데..

        from users import models as user_models
        host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)        로 사용해야하나.
        host = models.ForeignKey("users.User", on_delete=models.CASCADE)        이렇게 사용가능... ( 앱이름.모델클래스명 )

    https://nomadcoders.co/airbnb-clone/lectures/914

"""

""" 8.0
    review 에 Room 이 연결되어 있으므로 self.review_set.all() 으로 정보를 가져올수 있다.
    룸에 딸린 리뷰가 여러개일것이므로 for 문을 돌린다.
    각각의 리뷰안에 평균 점수를 내는 함수 rating_average() 사용
    점수를 가져와서 전부 더한후 전체 리뷰갯수로나눠준다.
"""
