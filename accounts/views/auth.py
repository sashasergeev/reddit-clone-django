from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.views import View


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You've logged in successfuly!")
            return redirect("main:index")
        else:
            return render(request, "registration/login.html", {"form": form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "You've successfully created an account!")
            return redirect("main:index")
        else:
            return render(request, "registration/register.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("main:index")
