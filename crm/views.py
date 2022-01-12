from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser

from .constants import SELLING_TEAM_NAME, SUPPORT_TEAM_NAME
from .serializers import UserSerializer, ClientSerializer, ContractSerializer, ContractStatusSerializer, EventSerializer
from .models import User, Client, Contract, ContractStatus, Event
from .permissions import (
    IsSuperUser,
    ClientListPermission, ClientDetailPermission,
    ContractListPermission, ContractDetailPermission,
    ContractStatusListPermission, ContractStatusDetailPermission,
    EventListPermission, EventDetailPermission
)


# USER LIST VIEW --------------------------------------------------------------

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = sorted(
        User.objects.all().filter(groups__name__in=[SELLING_TEAM_NAME, SUPPORT_TEAM_NAME]),
        key=lambda user: user.id
    )
    permission_classes = [IsSuperUser | IsAdminUser]


# CLIENT VIEWS ----------------------------------------------------------------

class ClientList(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ClientListPermission)]
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "email"]


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ClientDetailPermission)]


# CONTRACT VIEWS --------------------------------------------------------------

class ContractList(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ContractListPermission)]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "client__first_name", "client__last_name", "client__email",
        "date_created", "date_updated", "amount"
    ]


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ContractDetailPermission)]


# CONTRACT STATUS VIEWS -------------------------------------------------------

class ContractStatusList(generics.ListCreateAPIView):
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ContractStatusListPermission)]


class ContractStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ContractStatusDetailPermission)]


# EVENT VIEWS -----------------------------------------------------------------

class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & EventListPermission)]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "contract__client__first_name", "contract__client__last_name", "contract__client__email",
        "start_date", "end_date"
    ]


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & EventDetailPermission)]
