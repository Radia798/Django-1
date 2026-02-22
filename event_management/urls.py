"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path, include
# from django.urls import path
# from django.views import signup_view
# from django.contrib.auth import views as auth_views
# from django.views import ProfileView, ProfileUpdateView
# from django.contrib.auth import views as auth_views



# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("accounts/", include("accounts.urls")),
#     path("", include("events.urls")),

#     path("admin/", admin.site.urls),
#     path("accounts/", include("accounts.urls")),
#     path("users/", include("users.urls")),
#     path("", include("events.urls")),

#     path("admin/", admin.site.urls),                 # Admin panel
#     path("accounts/", include("accounts.urls")),    # signup, login, logout
#     path("users/", include("users.urls")),          # profile + password reset
#     path("", include("events.urls")), 


#     path("signup/", signup_view, name="signup"),
#     path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),

#      path("profile/", ProfileView.as_view(), name="profile"),
#     path("profile/edit/", ProfileUpdateView.as_view(), name="edit_profile"),

#     # Password change/reset
#     path("password-change/", auth_views.PasswordChangeView.as_view(template_name="users/password_change.html", success_url="/users/profile/"), name="password_change"),
#     path("password-reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
#     path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
#     path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
#     path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    
    
# ]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # Accounts app: signup, login, logout
    path("accounts/", include("accounts.urls")),

    # Users app: profile, edit, password change/reset
    path("users/", include("users.urls")),

    # Events app: event list, dashboard, CRUD, RSVP
    path("", include("events.urls")),
]

# Serve media files in development (profile pics, event images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)