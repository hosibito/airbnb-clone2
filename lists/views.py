from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(  # 리턴값 (object, created(bool))
            user=request.user, name="My Favourites Houses"  # 반환값이 한개 이상이면 에러
        )

        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
            # ManytoManyField라서 save()를 할필요가 없다.
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"

    # 찾을 필요가 없다.. 유저가 이미 리스트를 가지고 있기 떄문이다.!
