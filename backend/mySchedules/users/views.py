from django.shortcuts import render, redirect
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from users.models import User
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

@login_required
def home(request):

    return render(request, 'users/home.html')