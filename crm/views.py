from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .constants import SELLING_TEAM_NAME, SUPPORT_TEAM_NAME
from .serializers import ClientSerializer, ContractSerializer, ContractStatusSerializer, EventSerializer
from .models import Client, Contract, ContractStatus, Event


# OBJECTS ---------------------------------------------------------------------

def get_object(_class, pk):
    if _class not in (Client, Contract, ContractStatus, Event):
        raise TypeError
    try:
        instance = _class.objects.get(pk=pk)
    except _class.DoesNotExist:
        raise Http404
    else:
        return instance


# PERMISSION TESTS ------------------------------------------------------------

def is_superuser(user):
    return user.is_superuser


def is_member_of_selling_team(user):
    return user.groups.filter(name=SELLING_TEAM_NAME).exists()


def is_member_of_support_team(user):
    return user.groups.filter(name=SUPPORT_TEAM_NAME).exists()


def is_owning(user, object):
    if isinstance(object, Client):
        return user.id == object.contact.id
    elif isinstance(object, Contract):
        return is_owning(user, object.client)
    elif isinstance(object, ContractStatus):
        return is_owning(user, object.contract)
    elif isinstance(object, Event):
        return is_owning(user, object.contract) or object.support_contact.id == user.id
    return False


# CLIENT VIEWS ----------------------------------------------------------------

@method_decorator(staff_member_required, name="dispatch")
class ClientList(APIView):

    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if is_superuser(user) or is_member_of_selling_team(user):
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied


@method_decorator(staff_member_required, name="dispatch")
class ClientDetail(APIView):

    def get(self, request, pk, format=None):
        client = get_object(Client, pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        client = get_object(Client, pk)
        if is_superuser(user) or is_member_of_selling_team(user) and is_owning(user, client):
            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied

    def delete(self, request, pk, format=None):
        user = request.user
        if is_superuser(user):
            client = get_object(Client, pk)
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied


# CONTRACT VIEWS --------------------------------------------------------------

@method_decorator(staff_member_required, name="dispatch")
class ContractList(APIView):

    def get(self, request, format=None):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if is_superuser(user) or is_member_of_selling_team(user):
            serializer = ContractSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied


@method_decorator(staff_member_required, name="dispatch")
class ContractDetail(APIView):

    def get(self, request, pk, format=None):
        contract = get_object(Contract, pk)
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        contract = get_object(Contract, pk)
        if is_superuser(user) or (is_member_of_selling_team(user) and is_owning(user, contract)):
            serializer = ContractSerializer(contract, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied

    def delete(self, request, pk, format=None):
        user = request.user
        if is_superuser(user):
            contract = get_object(Contract, pk)
            contract.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied


# CONTRACT STATUS VIEWS -------------------------------------------------------

@method_decorator(staff_member_required, name="dispatch")
class ContractStatusList(APIView):

    def get(self, request, format=None):
        contract_status = ContractStatus.objects.all()
        serializer = ContractStatusSerializer(contract_status, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if is_superuser(user) or is_member_of_selling_team(user):
            serializer = ContractStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied


@method_decorator(staff_member_required, name="dispatch")
class ContractStatusDetail(APIView):

    def get(self, request, pk, format=None):
        contract_status = get_object(ContractStatus, pk)
        serializer = ContractStatusSerializer(contract_status)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        contract_status = get_object(ContractStatus, pk)
        if is_superuser(user) or is_member_of_selling_team(user) and is_owning(user, contract_status):
            serializer = ContractStatusSerializer(contract_status, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied

    def delete(self, request, pk, format=None):
        user = request.user
        if is_superuser(user):
            contract_status = get_object(ContractStatus, pk)
            contract_status.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied


# EVENT VIEWS -----------------------------------------------------------------

@method_decorator(staff_member_required, name="dispatch")
class EventList(APIView):

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if is_superuser(user) or is_member_of_selling_team(user) or is_member_of_selling_team(user):
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied


@method_decorator(staff_member_required, name="dispatch")
class EventDetail(APIView):

    def get(self, request, pk, format=None):
        event = get_object(Event, pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        event = get_object(Event, pk)
        if is_superuser(user) or is_owning(user, event) and (is_member_of_selling_team(user) or is_member_of_support_team(user)):
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied

    def delete(self, request, pk, format=None):
        user = request.user
        if is_superuser(user):
            event = get_object(Event, pk)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied
