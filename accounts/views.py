from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.


def LoginView(request):
    if request.user.is_authenticated:
        return redirect("main:index")

    if request.method != "POST":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main:index")

    context = {"form": form}
    return render(request, "registration/login.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("main:index")

    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("main:index")
    context = {"form": form}
    return render(request, "registration/register.html", context)


def LogoutView(request):
    logout(request)
    return redirect('main:index')