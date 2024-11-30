from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('makeShift/', views.makeShift_view, name='makeShift'),
    path('getShifts/', views.getShifts_view, name='getShift'),
    path('pickupShift/', views.pickupShift_view, name='pickupShift'),
    path("home/", views.home, name='home')
]
