from django.db import models
from django.db.models.expressions import RawSQL


class Car(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="cars/")
    address = models.TextField()
    price = models.FloatField()

    latitude = models.FloatField()
    longitude = models.FloatField()


    def get_locations_nearby_coords(latitude, longitude, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        # Great circle distance formula
        gcd_formula = """
                6371 * acos(
                    CASE
                        WHEN cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)) > 1 THEN 1
                        WHEN cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)) < -1 THEN -1
                        ELSE cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude))
                    END
                )
            """
        distance_raw_sql = RawSQL(
            gcd_formula,
            (latitude, longitude, latitude, latitude, longitude, latitude, latitude, longitude, latitude)
        )

        qs = Car.objects.all() \
        .annotate(distance=distance_raw_sql) \
        .order_by('distance')
        if max_distance is not None:
            qs = qs.filter(distance__lt=max_distance)
        return qs

    def __str__(self) -> str:
        return self.name
    




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
