from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Userprofile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

class Login(View):
    def get(self, request):
        return render(request, 'core/login.html')
    def post(self, request):
        user_id = request.POST.get("id").lower()
        password = request.POST.get("password")
        try:
            user_profile = Userprofile.objects.get(unique_id=user_id)
            user = authenticate(request, username=user_profile.user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid Password")
                return render(request, 'core/login.html')
        except Userprofile.DoesNotExist:
            messages.error(request, "Invalid user ID")
            return render(request, 'core/login.html')

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            auth_logout(request)
            return redirect('index')
        else:
            return redirect('login')

