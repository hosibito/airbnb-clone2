from django.core.management.base import BaseCommand

from rooms import models as room_models

# from rooms.models import Amenity
# 위는 사용할때 room_models.Amenity  로 사용해아 하나. 모델내부에 이름이 같은경우 어느모델에서 왓는지 명확해 짐으로 위에꺼를 사용한다.
NAME = "Amenities"


class Command(BaseCommand):  # 노트 9 참조
    help = f"{NAME} 더미데이터 생성"

    # def add_arguments(self, parser):
    #     parser.add_argument("--number", help=f"How many {NAME} do you want to create")

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for amenitie in amenities:
            room_models.Amenity.objects.create(name=amenitie)
            # Amenity.objects.create(name=amenitie)

        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} {NAME} created!!"))


"""
python manage.py seed_amenities
"""
