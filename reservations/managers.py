from django.db import models


class CustomReservationManager(models.Manager):  # 24.10 참고 사용안함 core로 옮김!!
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
