from django.core.management.base import BaseCommand

from rooms import models as room_models

# from rooms.models import Amenity
# 위는 사용할때 room_models.Amenity  로 사용해아 하나. 모델내부에 이름이 같은경우 어느모델에서 왓는지 명확해 짐으로 위에꺼를 사용한다.

NAME = "Facilities"


class Command(BaseCommand):  # 노트 9 참조
    help = f"{NAME} 더미데이터 생성"

    # def add_arguments(self, parser):
    #     parser.add_argument("--number", help=f"How many {NAME} do you want to create")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for facil in facilities:
            room_models.Facility.objects.create(name=facil)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} {NAME} created!!"))


"""
python manage.py seed_facilities
"""
