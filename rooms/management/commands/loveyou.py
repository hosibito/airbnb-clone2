from django.core.management.base import BaseCommand


class Command(BaseCommand):  # 9.0 참조

    help = "이 명령어는 사랑합니다 라고 말합니다. "

    # print("hello")

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        parser.add_argument(
            "--times",
            help="몇번이나 사랑한다고 말할까요?.",
        )

    def handle(self, *args, **options):
        # print(args, options)
        # # () {'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False,
        #          'no_color': False, 'force_color': False, 'times': '50'}
        # print("사랑합니다.")
        times = options.get("times")
        for t in range(0, int(times)):
            # print("i love you!")
            self.stdout.write(self.style.WARNING("i love you!"))


"""
python manage.py loveyou --times 50
"""
