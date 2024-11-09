from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('book_car/', views.book_car, name="book_car"),
    path('bookings/', views.bookings, name="bookings"),
    path('payment/<str:booking_id>/', views.payment, name="payment"),
    path('booking_info/<str:booking_id>/', views.booking_info, name="payment"),

    path('profile/', views.profile_page, name="profile"),
    
    path('support/', views.support, name="support"),
    path('admin_support/', views.admin_support, name="admin_support"),
    path('admin_support/<str:user_id>/', views.admin_support, name="admin_support"),


    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_successful/', views.payment_successful_view, name="payment_successful"),
    path('payment_failed/', views.payment_failed_view, name="payment_failed"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)