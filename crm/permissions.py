from rest_framework.permissions import BasePermission
from .constants import SELLING_TEAM_NAME, SUPPORT_TEAM_NAME


# SUPER USER PERMISSION -------------------------------------------------------

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


# CLIENT PERMISSIONS ----------------------------------------------------------

class ClientListPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "POST":
            if user.groups.filter(name=SELLING_TEAM_NAME).exists():
                return True

        return False


class ClientDetailPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "PUT":
            return user.groups.filter(name=SELLING_TEAM_NAME).exists()

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        client = obj

        if method == "GET":
            return True

        if method == "PUT":
            return user == client.contact


# CONTRACT PERMISSIONS --------------------------------------------------------

class ContractListPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "POST":
            return user.groups.filter(name=SELLING_TEAM_NAME).exists()

        return False


class ContractDetailPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "PUT":
            return user.groups.filter(name=SELLING_TEAM_NAME).exists()

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        contract = obj

        if method == "GET":
            return True

        if method == "PUT":
            return user == contract.client.contact

        return False


# CONTRACT STATUS PERMISSION --------------------------------------------------

class ContractStatusListPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "POST":
            return user.groups.filter(name=SELLING_TEAM_NAME).exists()

        return False


class ContractStatusDetailPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "PUT":
            return user.groups.filter(name=SELLING_TEAM_NAME).exists()

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        contract_status = obj

        if method == "GET":
            return True

        if method == "PUT":
            return user == contract_status.contract.client.contact

        return False


# EVENT PERMISSIONS -----------------------------------------------------------

class EventListPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "POST":
            return user.groups.filter(name__in=(SELLING_TEAM_NAME, SUPPORT_TEAM_NAME)).exists()

        return False


class EventDetailPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "GET":
            return True

        if method == "PUT":
            return user.groups.filter(name__in=(SELLING_TEAM_NAME, SUPPORT_TEAM_NAME)).exists()

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        event = obj

        if method == "GET":
            return True

        if method == "PUT":
            return user == event.contract.client.contact or user == event.support_contact

        return False
