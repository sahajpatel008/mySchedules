import datetime
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from users.models import User, UniqueShift
from django.core.mail import send_mail
from django.conf import settings

import random

# Create your views here.
@csrf_exempt
def register(request):
    print("Zinda hu mai")
    if request.method == 'POST':
        try:
            # Load data from request body
            data = json.loads(request.body)

            # Extract data from the request
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Simple validation (you can add more checks here)
            if not username or not email or not password:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already in use.'}, status=400)

            # Create the user
            user = User(
                username=username, 
                email=email,
                role='employee')
            user.set_password(password)
            user.save()

            # Send confirmation email
            send_mail(
                'Welcome to Our Website!',
                f'Hello {user.username}! Thanks for registering at our website.',
                settings.EMAIL_HOST_USER,  # From email (use your configured email)
                [user.email],  # To email (user's email)
                fail_silently=False,
            )

            # Return success response
            return JsonResponse({'message': f'Account created for {user.username} successfully.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
    # if request.method == 'POST':
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.set_password(form.cleaned_data['password'])
    #         user.save()

    #         # Send a confirmation email
    #         send_mail(
    #             'Welcome to Our Website!',
    #             f'Hello {user.username}! Thanks for registering at our website.',
    #             settings.EMAIL_HOST_USER,  # From email (use your configured email)
    #             [user.email],  # To email (user's email)
    #             fail_silently=False,
    #         )

    #         # login(request, user)
    #         messages.success(request, f'Account created for {user.username}!')
    #         return redirect('login')
    
    # form = UserRegisterForm()

    # return render(request, 'users/register.html', {'form': form })
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:    
            print("HELLO")
            data = json.loads(request.body)
            print(data)
            username = data.get("username")
            password = data.get("password")
            print("username:", username)
        
            if not username or not password:
                return JsonResponse({"error": "Username and password are required."}, status=400)

            user = authenticate(username=username, password=password)
        
            if user:
                paramsDict = {
                    "userID": user.username,
                    "number": 0
                }
                login(request, user)
                paramsDict['message'] = "Login successfull"
                

                if user.role == 'manager':
                    number = random.randint(1, 1000000)
                    paramsDict['number'] = number
                    return JsonResponse(paramsDict, status=200)
                    
                return JsonResponse(paramsDict, status=200)
                return JsonResponse({"message": "Login successful."}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except Exception as e:
            print("Exception is:", e)
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, f'Welcome back, {user.username}!')
    #             return redirect('home')  # Redirect to your home page
    #         else:
    #             messages.error(request, 'Invalid username or password.')
    
    # form = LoginForm()

    # return render(request, 'users/login.html', {'form': form})
@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully."}, status=200)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def makeShift_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            date = data.get("date")
            location = data.get("location")
            start_time = data.get("start_time")
            end_time = data.get("end_time")

            print("Date:", date)
            print("start_time:", start_time)
            print("end_time:", end_time)
            print("location:", location)

            if not all([date, location, start_time, end_time]):
                return JsonResponse({"Error": "date, location, start_time, end_time required"}, status=400)
            
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                print("date ban gai? Iski ban gai, teri nahi bani     (＞︿＜)")
                start_time = datetime.datetime.strptime(start_time, "%I:%M %p").time()
                end_time =datetime.datetime.strptime(end_time, "%I:%M %p").time()
                print("time ban gaya?")
            except ValueError:
                return JsonResponse({"error": "Invalid date or time format."}, status=400)
            
            # Ensure the shift start time is before the end time
            if start_time >= end_time:
                return JsonResponse({"error": "Start time must be before end time."}, status=400)
            
            # Create the shift
            shift = UniqueShift.objects.create(
                date=date,
                location=location,
                start_time=start_time,
                end_time=end_time,
            )
            return JsonResponse({"message": "shift created successfully", "shift_id": shift.shift_id}, status=201)

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


def getShifts_view(request):
    if request.method == "GET":
        try:
            # Retrieve all shifts from the database
            shifts = UniqueShift.objects.all()
            
            # Convert queryset to a list of dictionaries
            shifts_data = [
                {
                    "shift_id": shift.shift_id,
                    "employee": shift.user.username if shift.employee else None,
                    "manager": shift.user.username if shift.manager else None,
                    "date": shift.date.strftime("%Y-%m-%d"),
                    "location": shift.location,
                    "start_time": shift.start_time.strftime("%H:%M:%S"),
                    "end_time": shift.end_time.strftime("%H:%M:%S"),
                }
                for shift in shifts
            ]
            
            return JsonResponse({"shifts": shifts_data}, status=200)
        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@login_required
def home(request):

    return render(request, 'users/home.html')