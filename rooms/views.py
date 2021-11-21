from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "-create"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["time_now"] = now

        return context

        # print(context)
        # print(dir(context))
        # print(dir(context["page_obj"]))


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})


""" 12.2 함수형 detail view (404관련포함)
from django.http import Http404
from django.shortcuts import render

def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home")) # 12.2 참고
        raise Http404()

"""


""" 11 페이지1 100% 수동 참조
from math import ceil

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

"""


""" 11 페이지2 함수형 참조
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

### paginator의 구조를 파악하자
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    print(vars(rooms))
    print(dir(rooms))
    print(vars(rooms.paginator))
    print(dir(rooms.paginator)
    print(rooms.paginator)
    # <django.core.paginator.Paginator object at 0x000002AB93348430>
    print(rooms)  # <Page 1 of 12>

    return render(request, "rooms/home.html", context={"rooms": rooms})


### 함수 기본형
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10, orphans=4)
    # orphans=4 : 맨 마지막페이지의 object가 4개보다 작다면 그전페이지에 추가해서 보인다.
    # ex) 마지막 페이지에 3 개라면.. 마지막 페이지를 없애고 그전페이지에 13개를 보여준다.
    page_rooms = paginator.get_page(page)
    # Page범위를 벗어나거나 잘못된 페이지 번호를 처리하면서 지정된 1부터 시작하는 인덱스가 있는 개체를 반환.
    # 페이지가 숫자가 아니면 첫 번째 페이지를 반환, 음수이거나 페이지 수보다 크면 마지막 페이지를 반환

    return render(request, "rooms/home.html", context={"page_rooms": page_rooms})

### 함수 에러처리 완성형
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10, orphans=4)

    try:
        page_rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page_rooms": page_rooms})
    except EmptyPage:
        return redirect("/")
    except ValueError:
        return redirect("/")
"""
