from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Client, Contract, ContractStatus, Event
from .constants import SELLING_TEAM_NAME, SUPPORT_TEAM_NAME


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "mobile", "groups")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "mobile", "is_active", "is_staff", "groups")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "first_name", "last_name", "phone", "mobile", "is_staff")
    list_filter = ("is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations", {"fields": ("first_name", "last_name", "phone", "mobile",)}),
        ("Permissions", {"fields": ("is_staff", "groups", "is_superuser", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "phone", "mobile", "password1", "password2"),
        }),
    )
    search_fields = ("email", "first_name", "last_name",)
    ordering = ("email",)
    filter_horizontal = ()


class ClientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ClientAdmin, self).get_queryset(request)
        print("\n\n\n", request.resolver_match.func.__name__, "\n\n\n")
        if request.user.is_superuser:
            return queryset
        elif request.resolver_match.func.__name__ in ["changelist_view", "change_view"]:
            return queryset
        else:
            return queryset.filter(contact=request.user)

    def has_change_permission(self, request, obj=None):
        user = request.user
        has_permission = False

        if obj:
            if user.is_superuser:
                has_permission = True
            elif user.groups.filter(name=SELLING_TEAM_NAME).exists() and user.id == obj.contact.id:
                has_permission = True

        return has_permission

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contact":
            kwargs["queryset"] = User.objects.filter(groups__name=SELLING_TEAM_NAME)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContractAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ContractAdmin, self).get_queryset(request)
        print("\n\n\n", request.resolver_match.func.__name__, "\n\n\n")
        if request.user.is_superuser:
            return queryset
        elif request.resolver_match.func.__name__ in ["changelist_view", "change_view"]:
            return queryset
        else:
            return queryset.filter(client__contact=request.user)

    def has_change_permission(self, request, obj=None):
        user = request.user
        has_permission = False

        if obj:
            if user.is_superuser:
                has_permission = True
            elif user.groups.filter(name=SELLING_TEAM_NAME).exists() and user.id == obj.client.contact.id:
                has_permission = True

        return has_permission


class ContractStatusAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ContractStatusAdmin, self).get_queryset(request)
        print("\n\n\n", request.resolver_match.func.__name__, "\n\n\n")
        if request.user.is_superuser:
            return queryset
        elif request.resolver_match.func.__name__ in ["changelist_view", "change_view"]:
            return queryset
        else:
            return queryset.filter(contract__client__contact=request.user)

    def has_change_permission(self, request, obj=None):
        user = request.user
        has_permission = False

        if obj:
            if user.is_superuser:
                has_permission = True
            elif user.groups.filter(name=SELLING_TEAM_NAME).exists() and user.id == obj.contract.client.contact.id:
                has_permission = True

        return has_permission


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(EventAdmin, self).get_queryset(request)
        print("\n\n\n", request.resolver_match.func.__name__, "\n\n\n")
        if request.user.is_superuser:
            return queryset
        elif request.resolver_match.func.__name__ in ["changelist_view", "change_view"]:
            return queryset
        else:
            return queryset.filter(contract__client__contact=request.user)

    def has_change_permission(self, request, obj=None):
        user = request.user
        has_permission = False

        if obj:
            if user.is_superuser:
                has_permission = True
            elif user.groups.filter(name=SELLING_TEAM_NAME).exists() and user.id == obj.contract.client.contact.id:
                has_permission = True
            elif user.groups.filter(name=SUPPORT_TEAM_NAME).exists() and user.id == obj.support_contact.id:
                has_permission = True

        return has_permission

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "support_contact":
            kwargs["queryset"] = User.objects.filter(groups__name=SUPPORT_TEAM_NAME)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(Event, EventAdmin)
