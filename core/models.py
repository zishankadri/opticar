from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models import F, Func, FloatField, ExpressionWrapper
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin

from math import radians


class Car(models.Model):
    SEATS_CHOICES = [
        ('2', '2 seats'),
        ('4', '4 seats'),
        ('6', '6 seats'),
    ]
    MAKE_AND_MODEL_CHOICES = [
        ("Porsche", "Porsche"),
        ("Jaguar", "Jaguar"),
        ("Supra", "Supra"),
        ("Perodua Myvi", "Perodua Myvi"),
        ("Honda City", "Honda City"),
        ("Toyota Vios", "Toyota Vios"),
        ("Honda Civic", "Honda Civic"),
    ]
    CAR_TYPE_CHOICES = [
        ("SUV", "SUV"),
        ("Sedan", "Sedan"),
    ]

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cars/")
    seats = models.CharField(choices=SEATS_CHOICES, max_length=2)
    make_and_model = models.CharField(choices=MAKE_AND_MODEL_CHOICES, max_length=50)
    car_type = models.CharField(choices=CAR_TYPE_CHOICES, max_length=50)
    address = models.TextField()
    price = models.FloatField()

    latitude = models.FloatField()
    longitude = models.FloatField()



    def get_nearby_locations(lat, lon, max_distance=None):
        # Constants
        R = 6371.0  # Radius of the Earth in km
        lat = float(lat)
        lon = float(lon)
        # Convert latitude and longitude from degrees to radians
        lat_rad = radians(lat)
        lon_rad = radians(lon)

        # Annotate each location with the distance from the given point using the Haversine formula
        locations = Car.objects.annotate(
            distance=ExpressionWrapper(
                R * ACos(
                    Cos(Radians(lat)) * Cos(Radians(F('latitude'))) * Cos(Radians(F('longitude')) - lon_rad) +
                    Sin(Radians(lat)) * Sin(Radians(F('latitude')))
                ),
                output_field=FloatField()
            )
        ).order_by('distance')

        if max_distance is not None:
            locations = locations.filter(distance__lte=max_distance)

        return locations


    def __str__(self) -> str:
        return self.name
    

class Booking(models.Model):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"
    
    STATUC_CHOICES = [
        ("IN_PROGRESS", "In progress"),
        ("COMPLETE", "Complete"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)
    car = models.ForeignKey("core.Car", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUC_CHOICES, default=IN_PROGRESS, max_length=15)

    pick_up_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    drop_off_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)


    def get_duration_in_hours(self):
        # Calculate the difference between drop_off and pick_up
        duration = self.drop_off_datetime - self.pick_up_datetime
        # Convert duration to hours
        duration_in_hours = duration.total_seconds() / 3600
        return duration_in_hours
    
    def total_price(self):
        return self.get_duration_in_hours() * self.car.price
# For PostegresSQL

    # def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    #     """
    #     Return objects sorted by distance to specified coordinates
    #     which distance is less than max_distance given in kilometers
    #     """
    #     # Great circle distance formula
    #     gcd_formula = "6371 * acos(least(greatest(\
    #     cos(radians(%s)) * cos(radians(latitude)) \
    #     * cos(radians(longitude) - radians(%s)) + \
    #     sin(radians(%s)) * sin(radians(latitude)) \
    #     , -1), 1))"
    #     distance_raw_sql = RawSQL(
    #         gcd_formula,
    #         (latitude, longitude, latitude)
    #     )
    #     qs = Car.objects.all() \
    #     .annotate(distance=distance_raw_sql) \
    #     .order_by('distance')
    #     if max_distance is not None:
    #         qs = qs.filter(distance__lt=max_distance)
    #     return qs
