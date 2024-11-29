from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('makeShift/', views.makeShift_view, name='makeShift'),
    path("home/", views.home, name='home')
]
