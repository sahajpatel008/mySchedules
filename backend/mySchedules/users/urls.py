from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('makeShift/', views.makeShift_view, name='makeShift'),
    path('getShifts/', views.getShifts_view, name='getShift'),
    path('postedShifts/', views.getPostedShifts_view, name='postedShift'),
    path('pickupShift/', views.pickupShift_view, name='pickupShift'),
    path("getPickupRequests/", views.get_shift_requests_view,name='getPickup'),
    path('approvePickupRequests/', views.approve_shift_request_view, name='approveRequests'),
    path('getShifts_allUsers/', views.getshifts_allusers_view, name='getshifts_allusers'),
    path('getMyShifts/', views.myShifts, name='getMyShifts'),
    path("deleteShifts/", views.deleteShift_view, name='deleteShift'),
    path("home/", views.home, name='home')
]
