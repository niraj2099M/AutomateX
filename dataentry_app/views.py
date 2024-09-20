from . utils import get_all_custom_models
from django.http import HttpResponse

from django.core.management import call_command 


from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

# from app_dataentries.tasks import import_data_task
#from app_dataentries.tasks import export_data_task, import_data_task
from uploads_app.models import Upload





def import_data(request):
    """Import data"""
    if request.method == "POST":
        file_path = request.FILES.get("file_path") #uploaded csv file
        model_name = request.POST.get("model_name")

        # store this file inside the Upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # # construct the full path of file for command
        relative_path = str(upload.file.url) #/media/uploads/file.csv, Converted to str to concatenate
        base_url = str(settings.BASE_DIR)
        file_path = base_url + relative_path #absolute path of uploaded file



        try:
            call_command('importdata', file_path, model_name) #trigger any command from views
        except Exception as e:
            raise e 


        """
        # check for the csv errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("dataentries:import_data")

        # handle the import data task here
        import_data_task.delay(file_path, model_name)

        # show the message to the user
        messages.success(
            request,
            "Your data is being imported, you will be notified once it is done.",
        )"""
        return redirect("import_data")
    else:
        custom_models = get_all_custom_models()
        context = {
            "custom_models": custom_models,
        }
    return render(request, "dataentry_app/dataentry.html", context)


# def export_data(request):
#     if request.method == "POST":
#         model_name = request.POST.get("model_name")

#         # call the export data task
#         export_data_task.delay(model_name)

#         # show the message to the user
#         messages.success(
#             request,
#             "Your data is being exported, you will be notified once it is done.",
#         )
#         return redirect("dataentries:export_data")
#     else:
#         custom_models = get_all_custom_models()
#         context = {
#             "custom_models": custom_models,
#         }
#     return render(request, "app_dataentries/export_data.html", context)
