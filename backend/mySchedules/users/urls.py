from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('makeShift/', views.makeShift_view, name='makeShift'),
    path('getShifts/', views.getShifts_view, name='getShift'),   # used in available Shifts (user dashboard) tab, and requested Shifts tab.
    path('postedShifts/', views.getPostedShifts_view, name='postedShift'), # used in Posted Shift (schedules page) in manager.
    path('pickupShift/', views.pickupShift_view, name='pickupShift'),  #pickup shifts view where 
    path("getPickupRequests/", views.get_shift_requests_view,name='getPickup'),  # for a particular shift, it shows pickup requests in manager view
    path('approvePickupRequests/', views.approve_shift_request_view, name='approveRequests'), 
    path('getShifts_allUsers/', views.getshifts_allusers_view, name='getshifts_allusers'), # show a users*location matrix for a given date range
    path('getMyShifts/', views.myShifts, name='getMyShifts'), #show approved and requested shift for a particular username
    path("deleteShifts/", views.deleteShift_view, name='deleteShift'),
    path("home/", views.home, name='home')
]
