import csv

from django.apps import apps
from django.core.management.base import BaseCommand
from datetime import datetime



class Command(BaseCommand):
    """
    Propsed command = python manage.py exportdata model_name
    """
    help = "Export data from the database to a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"].capitalize()

        # search through all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # stop executing once the model is found
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model {model_name} cound not found")
            return

        # fetch the data from the database
        data = model.objects.all()

        #generate current datetime stamp
        timestamp=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # define csv file path
        file_path = f"exported_{model_name}_{timestamp}.csv"

        # open the csv file and write the data
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)

            # write the CSV header
            # we want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow(
                    [getattr(dt, field.name) for field in model._meta.fields]
                )

        self.stdout.write(self.style.SUCCESS("Data exported successfully!"))