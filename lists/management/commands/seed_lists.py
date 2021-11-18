import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "Lists"


class Command(BaseCommand):  # 노트 9 참조
    help = f"{NAME} 더미데이터 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"{NAME}을/를 number 만큼 생성합니다.",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "name": lambda x: seeder.faker.sentence(),
                "user": lambda x: random.choice(all_users),
            },
        )
        created_list = seeder.execute()
        created_list_pk_clean = flatten(list(created_list.values()))

        for pk in created_list_pk_clean:
            list_model = list_models.List.objects.get(pk=pk)
            # for room in all_rooms:  # manytomany가 너무 많으면... 문제
            #     magic_number = random.randint(0, 15)
            #     if magic_number % 2 == 0:
            #         list_model.rooms.add(room)
            f_r = random.randint(0, 5)
            l_r = random.randint(6, 15)
            to_add = all_rooms[f_r:l_r]
            # 배열에서 일정범위를 뽑아낸다. list[3:4]
            list_model.rooms.add(*to_add)  # 배열안에 요소를 집어넣는거이므로

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!!"))


"""
python manage.py seed_lists --number 20
"""
