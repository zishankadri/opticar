from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

import json

from .models import Car, Booking, Support_message
from .forms import CarFilterForm
from .search import smart_search
from datetime import timedelta
from .forms import CustomPayPalPaymentsForm
from accounts.models import UserAccount
from paypal.standard.forms import PayPalPaymentsForm


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
            # booking.save()

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
    today = timezone.now().date()
    pick_up_date = today.strftime('%m/%d/%Y')
    drop_off_date = (today + timedelta(days=1)).strftime('%m/%d/%Y')
    context = {
        'pick_up_date': pick_up_date,
        'drop_off_date': drop_off_date,
        'car_list': car_list,
        'recommended_cars': recommended_cars,
        'form': form,
    }
    return render(request, "home.html", context)


@login_required
@csrf_exempt
def book_car(request):
    if request.method == 'POST':
        if not request.user.verified_details:
            print("410 bberrrrrrrrrr")
            return JsonResponse({'is_verified_details': False}, status=410)
        
        data = json.loads(request.body)
        car_id = data.get('car_id')
        pick_up_date = data.get('pick_up_date')
        pick_up_time = data.get('pick_up_time')
        drop_off_date = data.get('drop_off_date')
        drop_off_time = data.get('drop_off_time')

        # Combine date and time into a single datetime object
        pick_up_datetime_str = f"{pick_up_date} {pick_up_time}"
        pick_up_datetime = datetime.strptime(pick_up_datetime_str, '%m/%d/%Y %H:%M')
        pick_up_datetime = timezone.make_aware(pick_up_datetime, timezone.get_current_timezone())

        drop_off_datetime_str = f"{drop_off_date} {drop_off_time}"
        drop_off_datetime = datetime.strptime(drop_off_datetime_str, '%m/%d/%Y %H:%M')
        drop_off_datetime = timezone.make_aware(drop_off_datetime, timezone.get_current_timezone())

        car = Car(id=car_id)

        booking = Booking(
            user = request.user,
            car = car,
            pick_up_datetime = pick_up_datetime,
            drop_off_datetime = drop_off_datetime
        )
        booking.save()

        return JsonResponse({'booking_id': booking.id, 'is_verified_details': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
def bookings(request):
    booking_list = Booking.objects.filter(user=request.user)
    
    context = {
        'booking_list': booking_list,
    }

    return render(request, "bookings.html", context)



@login_required
def payment(request, booking_id):
    if request.method == 'POST':
        if "cash_payment" in request.POST:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_method = Booking.CASH
            booking.status = Booking.IN_PROGRESS

            booking.save()

            return redirect('/bookings/')

    booking = Booking.objects.get(id=booking_id)
    total_hours = booking.get_duration_in_hours()
    total_price = total_hours * booking.car.price

    import uuid
    uid = str(uuid.uuid4()).replace("-", "")[:12]
    domain_name = request.build_absolute_uri('/')[:-1]


    form = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(total_price),
        "item_name": booking_id,
        "invoice": uid,

        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
        # Custom command to correlate to some function later (optional)
        "custom": request.user.id,
    }
    form = CustomPayPalPaymentsForm(initial=form, button_type="subscribe")

    context = {
        "form": form,
        "booking" : booking,
        "total_hours": total_hours,
    }

    return render(request, "payment.html", context)

    
def payment_successful_view(request):
    print("hello")
    return render(request, "payment.html")


def payment_failed_view(request):
    print("hello")

    return render(request, "payment.html")


@login_required
def bookings(request):
    booking_list = Booking.objects.filter(user=request.user)
    
    context = {
        'booking_list': booking_list,
    }

    return render(request, "bookings.html", context)


@login_required
def booking_info(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    total_hours = booking.get_duration_in_hours()

    context = {
        'booking' : booking,
        'total_hours': total_hours,
    }

    return render(request, "booking_info.html", context)



@login_required
def support(request):
    message_list = Support_message.objects.filter(user=request.user).order_by("date")
    if request.method == "POST":
        content = request.POST['content']
        message = Support_message(
            user=request.user,
            sender=request.user,
            content=content,
        )
        message.save()
        
    return render(request, "support.html", { 'message_list': message_list })



@login_required
def admin_support(request, user_id=None):
    if user_id:
        user = UserAccount.objects.get(id=user_id)
        message_list = Support_message.objects.filter(user=user).order_by("date")
        if request.method == "POST":
            content = request.POST['content']
            message = Support_message(
                user=user,
                sender=request.user,
                content=content,
            )
            message.save()
            
        return render(request, "support.html", { 'message_list': message_list })
    
    user_list = UserAccount.objects.all()
    context = {
        'user_list': user_list,
    }

    return render(request, "admin_support.html", context)


def profile_page(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']

        if request.FILES.get('ic'):
            ic = request.FILES['ic']
            request.user.ic = ic

        if request.FILES.get('license'):
            license = request.FILES['license']
            request.user.license = license

        request.user.full_name = full_name
        request.user.email = email
        request.user.save()

    return render(request, "profile.html")