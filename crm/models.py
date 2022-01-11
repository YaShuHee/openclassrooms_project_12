from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone=None, mobile=None, password=None,):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone=None, mobile=None, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            mobile=mobile,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = "Teammate"
        verbose_name_plural = "Teammates"

    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number_regex = RegexValidator(regex=r"0\d{9}")
    phone = models.CharField(validators=[phone_number_regex], max_length=10, blank=True, null=True)
    mobile = models.CharField(validators=[phone_number_regex], max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]   # for interactive user creation

    def clean(self):
        super().clean()
        if self.phone is None and self.mobile is None:
            raise ValidationError("At least one phone number must be set.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Client(models.Model):

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    phone_number_regex = RegexValidator(regex=r"0\d{9}")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(validators=[phone_number_regex], max_length=10, blank=True, null=True)
    mobile = models.CharField(validators=[phone_number_regex], max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=50)
    contact = models.ForeignKey(to="User", on_delete=models.DO_NOTHING, related_name="clients")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company_name})"

    def clean(self):
        super().clean()
        if self.phone is None and self.mobile is None:
            raise ValidationError("At least one phone number must be set.")


class Contract(models.Model):

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    reference = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    payment_due = models.DateTimeField()
    client = models.ForeignKey(to="Client", on_delete=models.CASCADE, related_name="contracts")

    def __str__(self):
        return f"{self.reference}"


class ContractStatus(models.Model):

    class Meta:
        verbose_name = "Contract Status"
        verbose_name_plural = "Contract Status"

    STATE_CHOICES = (
        ("S", "Started"),
        ("P", "Paused"),
        ("E", "Ended"),
    )
    is_accepted = models.BooleanField()
    acceptance_note = models.TextField(max_length=2000)
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    state_note = models.TextField(max_length=2000)
    contract = models.ForeignKey(to="Contract", on_delete=models.CASCADE, related_name="status")

    def __str__(self):
        return f"{'☑' if self.is_accepted else '☒'} {self.contract.reference} ({self.state})"


class Event(models.Model):

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    name = models.CharField(max_length=100)
    attendees = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    note = models.TextField(max_length=2000)
    contract = models.ForeignKey(to="Contract", on_delete=models.CASCADE, related_name="events")
    support_contact = models.ForeignKey(to="User", on_delete=models.DO_NOTHING, related_name="events")

    def __str__(self):
        if self.start_date.date() == self.end_date.date():
            start, end = self.start_date, self.end_date
            return f"{self.name} ({start.date()}, {start:%H:%M} to {end:%H:%M}) : {self.attendees} attendees"
        else:
            return f"{self.name} ({self.start_date.date()} to {self.end_date.date()}) : {self.attendees} attendees"
