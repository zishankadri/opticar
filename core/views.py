from django.shortcuts import render

from .models import Car


def home(request):
    if request.method == "POST":
        lat = request.POST['lat']
        lng = request.POST['lng']
        
        print(lat, "lng:", lng)

        car_list = Car.get_locations_nearby_coords(lat, lng)
        print(car_list)
        context = {
            'car_list': car_list,
        }

    else:
        car_list = Car.objects.all()
        print(car_list)

        context = {
            'car_list': car_list,
        }

    return render(request, "home.html", context)