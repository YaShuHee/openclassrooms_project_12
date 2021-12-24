from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class TeamMemberManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, phone, mobile, **extra_fields):
        if not email:
            raise ValueError("The email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        if phone is None and mobile is None:
            raise ValidationError("At least one of the two fields 'phone' or 'mobile' must be set.")
        user.phone = phone
        user.mobile = mobile
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Didn't find out how to keep basic superuser with a custom (non super)user. """
        if not email:
            raise ValueError("The email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class TeamMember(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = TeamMemberManager()

    def __str__(self):
        return self.email


class Client(models.Model):
    phone_number_regex = RegexValidator(regex=r"0\d{9}")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(validators=[phone_number_regex], max_length=10, null=True)
    mobile = models.CharField(validators=[phone_number_regex], max_length=10, null=True)
    company_name = models.CharField(max_length=50)
    contact = models.ForeignKey(to="TeamMember", on_delete=models.DO_NOTHING, related_name="clients")

    def clean(self):
        super().clean()
        if self.phone is None and self.mobile is None:
            raise ValidationError("At least one of the two fields 'phone' or 'mobile' must be set.")


class ContractStatus(models.Model):
    STATE_CHOICES = (
        ("S", "Started"),
        ("P", "Paused"),
        ("E", "Ended"),
    )
    is_accepted = models.BooleanField()
    acceptance_note = models.TextField(max_length=2000)
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    state_note = models.TextField(max_length=2000)


class Contract(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    payment_due = models.DateTimeField()
    client = models.ForeignKey(to="Client", on_delete=models.CASCADE, related_name="contracts")


class Event(models.Model):
    attendees = models.IntegerField()
    date = models.DateTimeField()
    note = models.TextField(max_length=2000)
    contract = models.ForeignKey(to="Contract", on_delete=models.CASCADE, related_name="events")
