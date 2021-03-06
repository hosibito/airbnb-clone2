from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries

from . import models, forms


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
    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        # 입력된 정보를 기억한다. bounded form 이 되어 데이터 무결성 검사를 하게된다.

        if form.is_valid():  # 폼 데이터가 무결성인지 알려준다.
            print(form.cleaned_data)
            # {'city': 'Anywhere', 'country': 'KR', ...
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            houserules = form.cleaned_data.get("houserules")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for amenitie in amenities:
                filter_args["amenities"] = amenitie

            for facilitie in facilities:
                filter_args["facilities"] = facilitie

            for houserule in houserules:
                filter_args["house_rules"] = houserule

            print(filter_args)

            rooms = models.Room.objects.filter(**filter_args)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

    else:
        form = forms.SearchForm()  # unbounded form

        return render(request, "rooms/search.html", {"form": form})


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
