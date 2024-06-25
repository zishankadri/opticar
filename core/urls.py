from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('book_car/', views.book_car, name="book_car"),
    path('bookings/', views.bookings, name="bookings"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)