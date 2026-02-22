from django import forms
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Category

# ----------------- User Signup Form -----------------
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

# ----------------- Category Form -----------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

# ----------------- Event Form -----------------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Exclude rsvp_users because users RSVP themselves
        exclude = ["rsvp_users", "created_by"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }