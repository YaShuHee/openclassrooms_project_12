from django.db import connection
from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import makemigrations, migrate, dumpdata, loaddata

from project.settings import DATABASES


def user_confirmed():
    choice = ""

    while choice not in ("y", "n"):
        choice = input("Confirm (y/n) ? ")

    return choice == "y"


class Command(BaseCommand):
    help = 'Totally flush the database and drop the tables. Rerun migrations and fixtures to repopulate it.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noprepopulate',
            action="store_true",
            help="Command will not prepopulate database."
        )
        parser.add_argument(
            '--y',
            action="store_true",
            help="Pass all confirmation (including security start confirmation)."
        )
        parser.add_argument(
            '--askconfirmation',
            action="store_true",
            help="Ask the user confirmation before every next step."
        )

    def handle(self, *args, **options):
        save_location = "crm/fixtures/last_saved.json"
        separator = "\n" + "-"*30 + "\n"
        new_line = "\n"

        # first confirmation --------------------------------------------------
        if not options["y"]:
            print("\n/!\\ UNSAFE FOR PRODUCTION /!\\\n")
            start_message = "This operation will :"\
                f"\n - drop all your actual '' database content"\
                f"(and save it into fixture file {save_location})"\
                "\n - execute the makemigrations command"\
                "\n - execute the migrate command"\
                + f"{f'{new_line}- prepopulate the database using fixtures' if not options['noprepopulate'] else ''}"\
                + f"{new_line}Your permission will{' not' if not options['askconfirmation'] else ''}"\
                + " be asked before each step.\n"
            print(start_message)
            if not user_confirmed():
                return
        """
        # saves all the actual data at 'crm/fixtures/last_saved.json' ---------
        print(separator + f"* Going to save you actual database content at {save_location}.")
        if options["askconfirmation"]:
            if not user_confirmed():
                return

        print("☐ Saving the actual database content.")
        management.call_command(dumpdata.Command(), output="crm/fixtures/last_saved.json")
        print("☑ Database content was saved into the 'crm/fixtures/last_saved.json' file."
              "Use 'manage.py loaddata last_saved.json' to restore it.")
        
        """

        # removes the PostgreSQL public schema and recreate it ----------------
        print(separator + "* Going to drop public schema and to create another.")
        if options["askconfirmation"]:
            if not user_confirmed():
                return

        with connection.cursor() as cursor:
            print("☐ Dropping the database public schema (and all the tables).")
            cursor.execute("DROP SCHEMA public CASCADE;")
            print("☑ Dropped the database public schema (and all the tables).")
            print("☐ Recreating the database public schema (without any table).")
            cursor.execute("CREATE SCHEMA public;")
            print("☑ Recreated the database public schema (without any table).")

        # makemigrations ------------------------------------------------------
        print(separator + "* Going to execute 'makemigrations' command.")
        if options["askconfirmation"]:
            if not user_confirmed():
                return

        print("☐ Executing makemigrations.")
        management.call_command(makemigrations.Command())
        print("☑ Executed makemigrations.")

        # migrate -------------------------------------------------------------
        print(separator + "* Going to execute 'migrate' command.")
        if options["askconfirmation"]:
            if not user_confirmed():
                return

        print(separator + "☐ Executing migrate.")
        management.call_command(migrate.Command())
        print("☑ Executed migrate.")

        # prepopulate ---------------------------------------------------------
        if not options["noprepopulate"]:
            print(separator + "* Going to prepopulate the database.")
            if options["askconfirmation"]:
                if not user_confirmed():
                    return

            print(separator + "☐ Prepopulating database with demo data.")
            fixtures = (
                "crm_user.json",
                "crm_client.json",
                "crm_contract.json",
                "crm_contract_status.json",
                "crm_event.json"
            )
            for file_name in fixtures:
                print(f"☐ Loading {file_name} fixture.")
                management.call_command(loaddata.Command(), file_name)
                print(f"☑ Loaded {file_name} fixture.")
            print("☑ Prepopulated database with demo data.")

        # Command end message -------------------------------------------------
        print("\n\n☑ Demo application is ready to use !")
