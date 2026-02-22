from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Event

# ---------------- RSVP Signal ----------------
@receiver(m2m_changed, sender=Event.rsvp_users.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":  # after RSVP is added
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            subject = f"RSVP Confirmation for {instance.name}"
            message = f"Hi {user.first_name},\nYou have successfully RSVPed for {instance.name}."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

# ---------------- Optional: Post-save for user activation ----------------
# This is optional if you already sent email in signup view
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Send activation email logic here if you prefer signals over views
        pass