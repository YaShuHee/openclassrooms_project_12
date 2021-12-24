from django.contrib import admin

from .models import TeamMember, Client, Contract, Event


admin.site.register(TeamMember)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
