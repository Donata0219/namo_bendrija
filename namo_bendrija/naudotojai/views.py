from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from .models import MyUser
from .forms import UserRegistrationForm, UserLoginForm

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            buto_numeris = form.cleaned_data['buto_numeris']
            user = MyUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                buto_numeris=buto_numeris,
                password=password
            )
            return redirect('home')
        return render(request, 'registration.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html', {'form': form})
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
