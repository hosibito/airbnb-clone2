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


"""  5.1 
    ForeignKey 에 정의된것을 {self.room.name} : {self.user.username} 식으로 불러올수 있다.
    self.room.host.username  같이 순환참조 가능
"""
