from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import SignupForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # email activation later
            user.save()

            # Assign Participant role by default
            participant_group, _ = Group.objects.get_or_create(name="Participant")
            user.groups.add(participant_group)

            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})
