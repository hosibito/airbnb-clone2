from django.core.management.base import BaseCommand

from rooms import models as room_models

# from rooms.models import Amenity
# 위는 사용할때 room_models.Amenity  로 사용해아 하나. 모델내부에 이름이 같은경우 어느모델에서 왓는지 명확해 짐으로 위에꺼를 사용한다.
NAME = "House Rules"


class Command(BaseCommand):  # 노트 9 참조
    help = f"{NAME} 더미데이터 생성"

    # def add_arguments(self, parser):
    #     parser.add_argument("--number", help=f"How many {NAME} do you want to create")

    def handle(self, *args, **options):
        house_rules = [
            "담배금지",
            "조용히",
            "쿵쿵대지 않기",
            "기물파손 금지",
            "룰룰룰1",
            "훔쳐가지마",
            "엿보지마",
        ]
        for house_rule in house_rules:
            room_models.HouseRule.objects.create(name=house_rule)
            # Amenity.objects.create(name=amenitie)

        self.stdout.write(self.style.SUCCESS(f"{len(house_rules)} {NAME} created!!"))


"""
python manage.py seed_house_rules
"""
