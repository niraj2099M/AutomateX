from django.core.management.base import BaseCommand,CommandError
from django.apps import apps
import csv


class Command(BaseCommand):
    """
    Proposed command - python manage.py importdata file_path model_name
    """

    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model_name"].capitalize()

        model=None
        for app_config in apps.get_app_configs(): #contains meta data of all apps
            try:
                model=apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue #model not found in current app so move to next app
        
        if not model:
            raise CommandError(f"Model '{model_name}' not found in any app!")

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully!"))