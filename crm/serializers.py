from rest_framework.serializers import ModelSerializer, ValidationError

from .constants import SELLING_TEAM_NAME, SUPPORT_TEAM_NAME
from .models import Client, Contract, ContractStatus, Event, User


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    def validate_contact(self, value):
        """ Check if the contact is in the Selling Team. """
        user = value
        if user.groups.filter(name=SELLING_TEAM_NAME).exists():
            return value
        raise ValidationError("The 'contact' must be a Selling Team member.")


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate_support_contact(self, value):
        """ Check if the contact is in the Selling Team. """
        user = value
        if user.groups.filter(name=SUPPORT_TEAM_NAME).exists():
            return value
        raise ValidationError("The 'support_contact' must be a Support Team member.")