from django.db import models
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    # guest = models.ForeignKey(
    #     "users.User", related_name="reservations", on_delete=models.CASCADE
    # )
    # room = models.ForeignKey(
    #     "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    # )

    def __str__(self):  #  5.2
        return f"{self.room} - {self.check_in}"

    """  5.2
        def __str__(self) 을 정의해주는이유
        admin 에서 list_display 를 설정해주면 안보이게 되나
        상단제목이나 consol.log 등 여러가지 불러오게 되는경우가 잇으므로 습관적으로 정의해주자.

    """
