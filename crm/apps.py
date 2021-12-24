from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

    def ready(self):
        from django.contrib.auth.models import Group, Permission

        selling_team, created = Group.objects.get_or_create(name="Selling team")
        selling_team.permissions.set([
            Permission.objects.get(codename="add_client"),
            Permission.objects.get(codename="change_client"),
            Permission.objects.get(codename="delete_client"),
            Permission.objects.get(codename="add_contract"),
            Permission.objects.get(codename="change_contract"),
            Permission.objects.get(codename="delete_contract"),
            Permission.objects.get(codename="add_event")
        ])

        support_team, created = Group.objects.get_or_create(name="Support team")
        support_team.permissions.set([
            Permission.objects.get(codename="change_event")
        ])
