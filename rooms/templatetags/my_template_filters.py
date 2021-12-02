from django import template

register = template.Library()


@register.filter
def sexy_capitals(value):
    print(value)
    return value + ":lalalalal"


@register.filter(name="sss2")
def sexy_capitals2(value):
    print(value)
    return value + ":lalalala1111l"


# 템플릿 필터의 기본개념 잡을것  24.4 참조
