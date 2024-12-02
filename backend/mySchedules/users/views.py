import datetime
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from users.models import Pickup, User, UniqueShift, Shift
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
                paramsDict['message'] = "Login successful"
                

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

@csrf_exempt
def getShifts_view(request):
    if request.method == "GET":
        try:
            # Retrieve the start_date and end_date from the query parameters
            print(request.GET)
            start_date_str = request.GET.get('start_date')  # e.g., "2024-11-01"
            end_date_str = request.GET.get('end_date')      # e.g., "2024-11-30"
            
            
            # Validate if both start_date and end_date are provided
            if not start_date_str or not end_date_str:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            # Convert the date strings into date objects

            start_timestamp_s = int(start_date_str) / 1000
            end_timestamp_s = int(end_date_str) / 1000
            # start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            # end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

            print(start_timestamp_s, end_timestamp_s)
            start_date = datetime.datetime.fromtimestamp(start_timestamp_s).date()
            end_date = datetime.datetime.fromtimestamp(end_timestamp_s).date()

            # Filter shifts within the date range and order them by date in ascending order
            shifts = UniqueShift.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')

            # Prepare the data for response
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

            # Return the shifts data as JSON response
            return JsonResponse({"shifts": shifts_data}, status=200)
        
        except ValueError as e:
            print("The exception:", e)
            return JsonResponse({"error": f"Invalid date format: {str(e)}"}, status=400)
        
        except Exception as e:
            print("The exception:", e)
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def pickupShift_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        employee_username = data.get("username")
        shift_id = int(data.get("shift_id"))

        try:
            # Get the related objects
            try:
                shift_obj = UniqueShift.objects.get(pk=shift_id)
            except UniqueShift.DoesNotExist:
                return JsonResponse({"error": "Shift not found."}, status=404)

            try:
                employee_obj = User.objects.get(pk=employee_username)
            except User.DoesNotExist:
                return JsonResponse({"error": "Employee not found."}, status=404)
            
            not_unique_shift_obj, created = Shift.objects.get_or_create(
                shift_id = shift_obj,
                employee = employee_obj,
                defaults={'status': "Request"}
            )

            if not created:
                return JsonResponse({"message": "shift pickup request already exists."}, status=400)
            
            Pickup.objects.create(
                shift=shift_obj,
                employee=employee_obj,
                request_status= 'Request'
            )
            
            
            return JsonResponse({"message": "shift pickup request sent", "pickup_id": shift_obj.pk}, status=201)

            

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
        
@csrf_exempt
def get_shift_requests_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            req_shift_id = int(data.get("shift_id"))

            if not req_shift_id:
                return JsonResponse({"error": "Shift ID is required."}, status=400)

            req_shift_id = int(req_shift_id)
            
            shift_status = 0
            # check if shift status is approved to any user or not
            if Shift.objects.filter(shift_id=req_shift_id, status="Approved").exists():
                shift_status = 1
            
            emp = Shift.objects.get(shift_id=req_shift_id, status="Approved")

            # Get all requests for the given shift ID
            if shift_status == 0:
                shift_requests = Shift.objects.filter(shift_id=req_shift_id, status="Request")
                requests_data = [
                {"username": shift.employee.username, "shift_request_id": shift.pk, "shift_status": shift_status}
                for shift in shift_requests
                ]
            else:
                requests_data = {"username":emp.employee.username, "shift_request_id": emp.pk, "shift_status": shift_status}
            
            # Prepare the data to return            

            return JsonResponse({"requests": requests_data}, status=200)

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def approve_shift_request_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            shift_request_id = data.get("shift_request_id")
            employee_id = data.get("employee_id")

            print(data)

            if not shift_request_id or not employee_id:
                return JsonResponse({"error": "Shift request ID and employee ID is required."}, status=400)
            
            shift_request_id = int(shift_request_id)
            

            # Get the shift request object
            try:
                # shift_obj = Shift.objects.filter(shift_id=shift_request_id)
                # employee_obj = User.objects.filter(username=employee_id)
                approved_request = Shift.objects.filter(shift_id=shift_request_id, employee=employee_id)
            except Shift.DoesNotExist:
                return JsonResponse({"error": "Shift request not found or already processed."}, status=404)

            # Update the approved request status to "approved"
            approved_request.update(status='Approved')
            Shift.objects.filter(shift_id=shift_request_id).exclude(employee=employee_id).update(status='Denied')

            return JsonResponse({"message": "Shift request approved successfully. Other requests declined."}, status=200)

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
            

@login_required
def home(request):

    return render(request, 'users/home.html')