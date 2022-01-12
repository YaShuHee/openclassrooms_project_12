from django.urls import path

from .views import (
    UserList,
    ClientList, ClientDetail,
    ContractList, ContractDetail,
    ContractStatusList, ContractStatusDetail,
    EventList, EventDetail
)


urlpatterns = [
    path('user/', UserList.as_view()),
    path('client/', ClientList.as_view()),
    path('client/<int:pk>/', ClientDetail.as_view()),
    path('contract/', ContractList.as_view()),
    path('contract/<int:pk>/', ContractDetail.as_view()),
    path('contract_status/', ContractStatusList.as_view()),
    path('contract_status/<int:pk>/', ContractStatusDetail.as_view()),
    path('event/', EventList.as_view()),
    path('event/<int:pk>/', EventDetail.as_view()),
]
