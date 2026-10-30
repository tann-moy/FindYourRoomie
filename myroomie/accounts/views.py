
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import UserProfile, Preference
from .forms import RegisterForm, ProfileForm, PreferenceForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                name=form.cleaned_data["name"]
            )

            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username}
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": profile}
    )


@login_required
def preferences_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username}
    )

    preference = Preference.objects.filter(
        user=profile
    ).first()

    if request.method == "POST":
        form = PreferenceForm(
            request.POST,
            instance=preference
        )

        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = profile
            preference.save()
            return redirect("preferences")
    else:
        form = PreferenceForm(instance=preference)

    return render(
        request,
        "accounts/preferences.html",
        {"form": form}
    )
