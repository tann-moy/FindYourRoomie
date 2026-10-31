from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile, Preference

from .matching_algorithm import calculate_compatibility


@login_required
def matches_view(request):

    # Get the current user's profile.
    my_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username
        }
    )

    # Get current user's preferences.
    my_preference = Preference.objects.filter(
        user=my_profile
    ).first()

    # Require the current user to save preferences.
    if my_preference is None:
        return render(
            request,
            "matching/matches.html",
            {
                "matches": [],
                "preferences_missing": True,
            }
        )

    # Get other users' preferences.
    other_preferences = (
        Preference.objects
        .exclude(user=my_profile)
        .select_related("user", "user__user")
    )

    matches = []

    for other_preference in other_preferences:

        other_profile = other_preference.user

        if other_profile is None:
            continue

        if other_profile.user is None:
            continue

        if not other_profile.user.is_active:
            continue

        # Do not show the current user as their own match.
        if other_profile.user_id == request.user.id:
            continue

        # Calculate compatibility.
        result = calculate_compatibility(
            my_preference,
            other_preference,
            my_profile,
            other_profile
        )

        score = result["score"]

        # Show only users with at least 70% compatibility.
        if score >= 70:
            matches.append({
                "profile": other_profile,
                "score": score,
                "details": result["details"],
                "compared_factors": result["compared_factors"],
            })

    # Highest score first.
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return render(
        request,
        "matching/matches.html",
        {
            "matches": matches,
            "preferences_missing": False,
        }
    )
