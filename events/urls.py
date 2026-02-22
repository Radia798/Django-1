from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Event CRUD
    path("", views.event_list, name="event_list"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("add/", views.event_create, name="event_create"),
    path("edit/<int:event_id>/", views.event_update, name="event_update"),
    path("delete/<int:event_id>/", views.event_delete, name="event_delete"),

    # RSVP
    path("event/<int:event_id>/rsvp/", views.rsvp_event, name="rsvp_event"),
 
]