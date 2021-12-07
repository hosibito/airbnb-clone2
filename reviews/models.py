from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    # user = models.ForeignKey(
    #     "users.User", related_name="reviews", on_delete=models.CASCADE
    # )
    # room = models.ForeignKey(
    #     "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    # )

    def __str__(self):
        return f"{self.review} - {self.room}"
        # self.room.country  => KR (같은게 가능) 5.1 참조

    def rating_average(self):  # 2 참조
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "평점평균"

    class Meta:
        ordering = ("-create",)


"""  5.1 
    ForeignKey 에 정의된것을 {self.room.name} : {self.user.username} 식으로 불러올수 있다.
    self.room.host.username  같이 순환참조 가능
"""

""" 2
    함수로 표시될수 있는것을 만들수 있다.
    model 에 만들면 전체에서 다 이용하가능하고
    admin 에서 만들면 admin 에서만 이용가능하다.
"""
