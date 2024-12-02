import datetime
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import timedelta
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
                paramsDict['username'] = username

                if user.role == 'manager':
                    
                    number = random.randint(1, 1000000)
                    paramsDict['number'] = number
                    paramsDict['user'] = 'manager'
                    return JsonResponse(paramsDict, status=200)
                
                paramsDict['user'] = 'employee'
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
            # print(request.GET)
            start_date_str = request.GET.get('start_date')  # e.g., "2024-11-01"
            end_date_str = request.GET.get('end_date')      # e.g., "2024-11-30"
            
            
            # Validate if both start_date and end_date are provided
            if not start_date_str or not end_date_str:
                return JsonResponse({"error": "Both start_date and end_date are required."}, status=400)

            # Convert the date strings into date objects
            # print(start_date_str, type(start_date_str))
            start_date = datetime.datetime.fromtimestamp(int(float(start_date_str))).date()
            end_date = datetime.datetime.fromtimestamp(int(float(end_date_str))).date()

            # print(start_date, end_date)

            # # Filter shifts within the date range and order them by date in ascending order
            # shifts = UniqueShift.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')

            # # Prepare the data for response
            # shifts_data = [
            #     {
            #         "shift_id": shift.shift_id,
            #         "employee": shift.user.username if shift.employee else None,
            #         "manager": shift.user.username if shift.manager else None,
            #         "date": shift.date.strftime("%Y-%m-%d"),
            #         "location": shift.location,
            #         "start_time": shift.start_time.strftime("%H:%M:%S"),
            #         "end_time": shift.end_time.strftime("%H:%M:%S"),
            #     }
            #     for shift in shifts
            # ]

            # Initialize an empty list to hold the data
            shifts_data = []

            # Iterate over the range of dates
            current_date = start_date
            while current_date <= end_date:
                # Query shifts for the current date
                shifts = UniqueShift.objects.filter(date=current_date).order_by('date')

                # Prepare the shift data for the current date
                date_shifts = {
                    "date": current_date.strftime("%m/%d/%Y"),
                    "data": [
                        {
                            "user": shift.employee.username if shift.employee else None,
                            "start_time": shift.start_time.strftime("%I:%M %p"),
                            "end_time": shift.end_time.strftime("%I:%M %p"),
                            "location": shift.location
                        }
                        for shift in shifts
                    ]
                }

                # Append the data for the current date to the list
                shifts_data.append(date_shifts)

                # Move to the next day
                current_date += timedelta(days=1)

            # Return the shifts data as a JSON response
            return JsonResponse({"data": shifts_data})


            # # Filter shifts within the date range and order them by date in ascending order
            # shifts = UniqueShift.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')

            # # Create a dictionary with all dates in the range as keys
            # shifts_data = { 
            #     (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"): []
            #     for i in range((end_date - start_date).days + 1)
            # }

            # # Populate the dictionary with shift data
            # for shift in shifts:
            #     date_key = shift.date.strftime("%Y-%m-%d")
            #     shifts_data[date_key].append({
            #         "shift_id": shift.shift_id,
            #         "employee": shift.employee.username if shift.employee else None,
            #         "manager": shift.manager.username if shift.manager else None,
            #         "date": shift.date.strftime("%Y-%m-%d"),
            #         "location": shift.location,
            #         "start_time": shift.start_time.strftime("%H:%M:%S"),
            #         "end_time": shift.end_time.strftime("%H:%M:%S"),
            #     })

            # # Return the shifts data as JSON response
            # return JsonResponse({"shifts": shifts_data}, status=200)
        
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

@csrf_exempt
def getshifts_allusers_view(request):
    if request.method == 'GET':
        try:
            # Extract data from the request
            # data = json.loads(request.body)
            # print(data)
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            location = request.GET.get('location')
            # print(start_date)
            # format_string = "%Y-%m-%d"
            # start_date = datetime.datetime.strptime(start_date, format_string)
            start_date = datetime.datetime.fromtimestamp(start_date).date()
            end_date = datetime.datetime.fromtimestamp(end_date).date()
            # end_date = datetime.datetime.strptime(end_date, format_string)
            
  

            if not all([start_date, end_date, location]):
                return JsonResponse({"error": "Missing required fields: start_date, end_date, or location"}, status=400)

            # Query all shifts in the range and location
            # shifts = UniqueShift.objects.filter(
            #     date__gte = start_date, 
            #     date__lte = end_date,
            #     location = location
            # )

            # print("lol idhar ",shifts)
            # Get all users who have been assigned at least one shift in the location and range
            employees = list(User.objects.filter(role="employee"))

            # Prepare a response dictionary where each user is a key
            response_data = {}
            all_dates = []
            current_date = start_date
            while current_date <= end_date:
                all_dates.append(current_date)
                current_date += timedelta(days=1)
            # print("kidhar ",employees)
            for user in employees:
                user_shifts = UniqueShift.objects.filter(
                    date__gte = start_date, 
                    date__lte = end_date,
                    location = location,
                    employee_id=user
                )
                # print(user_shifts)
                # Group shifts by date, allowing multiple shifts on the same day
                shifts_by_date = {}
                for shift in user_shifts:
                    if shift.date not in shifts_by_date:
                        # print("Jana phut")
                        shifts_by_date[shift.date] = []
                    shifts_by_date[shift.date].append({
                        "shift_id": shift.shift_id,
                        "start_time": shift.start_time,
                        "end_time": shift.end_time
                    })
                    # print("Yeh dekho ",shifts_by_date)

                # Add all dates to the response, including empty ones
                # print("Saari dates", all_dates)
                user_shifts_with_empty_dates = []
                for date in all_dates:
                    date = date.date()
                    if date in shifts_by_date:
                        user_shifts_with_empty_dates.append(shifts_by_date[date])
                    else:
                        user_shifts_with_empty_dates.append([])  # Empty list for dates with no shifts
                print(user_shifts_with_empty_dates)
                response_data[user.username] = user_shifts_with_empty_dates
            # print(employees)
            return JsonResponse({"data": response_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def home(request):

    return render(request, 'users/home.html')