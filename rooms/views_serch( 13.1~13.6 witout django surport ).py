from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries

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
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    # s_amenities = request.GET.get("amenities")
    # s_facilities = request.GET.get("facilities")
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    s_house_rules = request.GET.getlist("house_rules")

    print(s_amenities, s_facilities)

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "s_house_rules": s_house_rules,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    house_rules = models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:  # !!!!
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


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
