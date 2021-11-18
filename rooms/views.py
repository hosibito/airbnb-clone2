from datetime import datetime
from django.shortcuts import render

# from django.http import HttpResponse


def all_rooms(request):
    # print(request)
    # print(vars(request))
    # print(dir(request))

    # now = datetime.now()
    # return HttpResponse(content=f"<h1>{now}</h1>")
    # return render(request, "all_rooms")

    now = datetime.now()
    hungry = True
    return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
