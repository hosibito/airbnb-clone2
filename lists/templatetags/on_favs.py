from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):  # context 그 html 페이지의 모든정보를 가지고 있다.
    user = context.request.user
    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )
    return room in the_list.rooms.all()
