from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Car, Booking
from .forms import CarFilterForm

from django.utils.dateparse import parse_date, parse_time
from datetime import datetime
from django.utils import timezone

from .search import smart_search

@login_required
def home(request):
    initial_data = {'location': request.GET.get('location')}
    form = CarFilterForm(request.POST or None, initial=initial_data)

    if request.method == "POST":
        if "booking" in request.POST:
            pick_up_date = request.POST['pick_up_date']
            pick_up_time = request.POST['pick_up_time']
            drop_off_date = request.POST['drop_off_date']
            drop_off_time = request.POST['drop_off_time']

            # Combine date and time into a single datetime object
            try:
                pick_up_datetime_str = f"{pick_up_date} {pick_up_time}"
                pick_up_datetime = datetime.strptime(pick_up_datetime_str, '%m/%d/%Y %H:%M')
                pick_up_datetime = timezone.make_aware(pick_up_datetime, timezone.get_current_timezone())

                drop_off_datetime_str = f"{drop_off_date} {drop_off_time}"
                drop_off_datetime = datetime.strptime(drop_off_datetime_str, '%m/%d/%Y %H:%M')
                drop_off_datetime = timezone.make_aware(drop_off_datetime, timezone.get_current_timezone())
            except:
                pick_up_datetime = timezone.now()
                drop_off_datetime = timezone.now()

            print(pick_up_datetime)
            print(drop_off_datetime)
            print("------------------")

            car_id = request.POST['car_id']
            car = Car(id=car_id)

            booking = Booking(
                user = request.user,
                car = car,
                pick_up_datetime = pick_up_datetime,
                drop_off_datetime = drop_off_datetime
            )
            booking.save()

        if "filter" in request.POST or "search" in request.POST:
            pick_up_date = request.POST.get('pick_up_date')
            pick_up_time = request.POST.get('pick_up_time')
            drop_off_date = request.POST['drop_off_date']
            drop_off_time = request.POST['drop_off_time']
            lat = request.POST['lat']
            lng = request.POST['lng']    

            print(drop_off_time)
            print(pick_up_time)

            recommended_cars = smart_search(request.user, lat, lng)
            print("recommended_cars", recommended_cars)

            if form.is_valid():
                location = form.cleaned_data.get('location')
                seats = form.cleaned_data.get('seats')
                make_and_model_list = form.cleaned_data.get('make_and_model')
                car_type_list = form.cleaned_data.get('car_type')

                print(form.cleaned_data)

                car_list = Car.get_nearby_locations(lat, lng)
                if seats:
                    car_list = car_list.filter(seats__in=seats)
                    recommended_cars = recommended_cars.filter(seats__in=seats)
                    
                if make_and_model_list:
                    car_list = car_list.filter(make_and_model__in=make_and_model_list)
                    recommended_cars = recommended_cars.filter(make_and_model__in=make_and_model_list)
                if car_type_list:
                    car_list = car_list.filter(car_type__in=car_type_list)
                    recommended_cars = recommended_cars.filter(car_type__in=car_type_list)

                context = {
                    'recommended_cars': recommended_cars,
                    'car_list': car_list,
                    'lat': lat,
                    'lng':lng,
                    'form': form,
                    'pick_up_date': pick_up_date,
                    'pick_up_time': pick_up_time,
                    'drop_off_date': drop_off_date,
                    'drop_off_time': drop_off_time,
                }
                return render(request, "home.html", context)
                
            else: print(form.errors)


    car_list = Car.get_nearby_locations(4.2105, 101.9758)
    recommended_cars = smart_search(request.user, 4.2105, 101.9758)

    context = {
        'pick_up_date': timezone.now().day,
        'drop_off_date': timezone.now().day+1,
        'car_list': car_list,
        'recommended_cars': recommended_cars,
        'form': form,
    }
    return render(request, "home.html", context)


@csrf_exempt
def booking(request):
    print("hello")
    print("hello")
    
    print(request.POST)

    return redirect('/')

