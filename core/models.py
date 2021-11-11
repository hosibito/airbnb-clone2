from django.db import models

"""
모든곳에 공통으로 쓰일 모델 
이 모델 자체가 DB로 가지 않는다. (반복작업을 안하기 위한것일뿐)
그래서 abstract = True 옵션을 준다. (확장사용을 위한 모델)
"""


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
