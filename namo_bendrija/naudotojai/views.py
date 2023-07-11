from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import MyUser


class UserRegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        buto_numeris = request.POST.get('buto_numeris')
        password = request.POST.get('password')

        if email and password:
            user = MyUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                buto_numeris=buto_numeris,
                password=password
            )
            login(request, user)
            return redirect('vartotojo_profilis')

        return render(request, 'registration.html')

class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('vartotojo_profilis')

        return render(request, 'login.html')

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html')


def vartotojo_profilis(request):
       return render(request, 'vartotojo_profilis.html', {'user': request.user})
