from django.db import models
from django.utils import timezone  # 8.1

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

    def __str__(self):  # 5.2
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in <= now and now <= self.check_out

    in_progress.boolean = True  # x 기호로 표시

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True  # x 기호로 표시

    """  5.2
        def __str__(self) 을 정의해주는이유
        admin 에서 list_display 를 설정해주면 안보이게 되나
        상단제목이나 consol.log 등 여러가지 불러오게 되는경우가 잇으므로 습관적으로 정의해주자.

    """

    """ 8.1
        장고에서는 파이선 Time 를 쓰지 않는다. 장고에서 관리하는
        TIME_ZONE = "Asia/Seoul" 기준시간을 사용할수 있게하기 위해(서버시간을 가져와서 저 설정에 맞는 시간으로 고쳐진다. )
        어플리케이션 서버의 타임을 알고있기를 원하니까.
    """
