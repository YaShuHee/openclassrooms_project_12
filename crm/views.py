from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import ClientSerializer, ContractSerializer, ContractStatusSerializer, EventSerializer
from .models import Client, Contract, ContractStatus, Event
from .permissions import (
    IsSuperUser,
    ClientListPermission, ClientDetailPermission,
    ContractListPermission, ContractDetailPermission,
    ContractStatusListPermission, ContractStatusDetailPermission,
    EventListPermission, EventDetailPermission
)


# CLIENT VIEWS ----------------------------------------------------------------

class ClientList(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ClientListPermission)]


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ClientDetailPermission)]


# CONTRACT VIEWS --------------------------------------------------------------

class ContractList(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & ContractListPermission)]


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


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsSuperUser | (IsAdminUser & EventDetailPermission)]
