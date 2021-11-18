from math import ceil
from django.shortcuts import render

from . import models


def all_rooms(request):
    # page = int(request.GET.get("page", 1))  # 주소창에 페이지 번호를 안넣으면 에러
    page = request.GET.get("page", 1)  # 아예 아무것도 입력안할떄 1 ?page=  로 입력이 들어오면 "" 반환.
    page = int(page or 1)  # page가 "" 라면 1 반환.

    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]

    page_count = ceil(models.Room.objects.count() / page_size)  # 올림
    return render(
        request,
        "rooms/home.html",
        {
            "potato": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
