from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
import requests
import pandas as pd
from .forms import CustomUserCreationForm, CustomUserLoginForm

# Get the custom user model
CustomUser = get_user_model()

# Function to send OTP
def send_otp(mobile):
    api_key = settings.TWO_FACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/AUTOGEN"
    response = requests.get(url)
    return response.json()

# Function to verify OTP
def verify_otp(session_id, otp_input):
    api_key = settings.TWO_FACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_input}"
    response = requests.get(url)
    return response.json()

# Function-based view for user registration
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create and save the new user
            login(request, user)  # Log the user in
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

# Function-based view for user login
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Change 'home' to an existing URL pattern name
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

# Function-based view for OTP login
def otp_login_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if 'otp' in request.POST:  # OTP verification step
            session_id = request.session.get('otp_session_id')
            otp = request.POST.get('otp')
            verification_response = verify_otp(session_id, otp)
            if verification_response.get('Status') == 'Success':
                # Redirect to home page regardless of whether the user is found
                return redirect('home')
            else:
                return render(request, 'otp_login.html', {'error': 'Invalid OTP', 'mobile': mobile})
        else:  # OTP sending step
            otp_response = send_otp(mobile)
            if otp_response.get('Status') == 'Success':
                request.session['otp_session_id'] = otp_response.get('Details')
                return render(request, 'otp_login.html', {'mobile': mobile})
            else:
                return render(request, 'otp_login.html', {'error': 'Failed to send OTP'})
    else:
        return render(request, 'otp_login.html')

# Function-based view for the home page
def home_view(request):
    excel_data = None

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            # Read the Excel file using pandas
            df = pd.read_excel(excel_file, engine='openpyxl')  # Explicitly use openpyxl for .xlsx files

            # Convert the DataFrame to a dictionary to pass to the template
            excel_data = {
                'headers': df.columns.tolist(),
                'rows': df.values.tolist()
            }

        except Exception as e:
            excel_data = {'error': str(e)}

    return render(request, 'home.html', {'excel_data': excel_data})
