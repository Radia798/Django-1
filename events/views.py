from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils.timezone import now

from .models import Event, Category
from .forms import EventForm, SignupForm

# ---------------- RBAC helper functions ----------------
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

# ---------------- Authentication ----------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate until email activation
            user.save()
            # Add to Participant group
            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)

            # Send activation email
            current_site = request.get_host()
            subject = 'Activate your Event Management Account'
            message = render_to_string('events/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
            return render(request, 'events/activation_sent.html')
    else:
        form = SignupForm()
    return render(request, 'events/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'events/activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'events/login.html', {'error': 'Account not activated.'})
        else:
            return render(request, 'events/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'events/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------- Dashboards ----------------
@login_required
def dashboard(request):
    today = now().date()
    user = request.user

    if is_admin(user):
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(date__gt=today).count()
        past_events = Event.objects.filter(date__lt=today).count()
        today_events = Event.objects.filter(date=today)
        context = {
            "total_events": total_events,
            "upcoming_events": upcoming_events,
            "past_events": past_events,
            "today_events": today_events,
        }
        return render(request, "events/admin_dashboard.html", context)

    elif is_organizer(user):
        # Organizer can see only their events
        events = Event.objects.filter(created_by=user)
        context = {"events": events}
        return render(request, "events/organizer_dashboard.html", context)

    else:
        # Participant dashboard: show RSVP'd events
        rsvped_events = user.rsvp_events.all()
        context = {"rsvped_events": rsvped_events}
        return render(request, "events/participant_dashboard.html", context)

# ---------------- Event Views ----------------
@login_required
def event_list(request):
    search = request.GET.get("search", "")
    events = Event.objects.select_related("category").filter(
        Q(name__icontains=search) | Q(location__icontains=search)
    )
    return render(request, "events/event_list.html", {"events": events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})

@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/form.html", {"form": form})

@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/form.html", {"form": form})

@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect("event_list")

# ---------------- RSVP ----------------
@login_required
@user_passes_test(is_participant)
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.rsvp_users.all():
        event.rsvp_users.add(request.user)
        # Send confirmation email
        subject = f"RSVP Confirmation for {event.name}"
        message = f"Hi {request.user.first_name},\nYou have successfully RSVPed for {event.name}."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email], fail_silently=False)
    return redirect("dashboard")