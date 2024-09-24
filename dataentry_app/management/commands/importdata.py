from django.core.management.base import BaseCommand,CommandError
from django.apps import apps
import csv
from django.db import DataError

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
        #getting the dynamic model
        for app_config in apps.get_app_configs(): #contains meta data of all apps
            try:
                model=apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue #model not found in current app so move to next app
        
        if not model:
            raise CommandError(f"Model '{model_name}' not found in any app!")

        #get all the field name of the found model excluding id
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        


        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            #error handling for wring selected model
            if csv_header != model_fields:
                raise DataError(f"CSV file doesnt match with the {model_name} table fields.")

            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully!"))