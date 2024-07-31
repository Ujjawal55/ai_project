from django.shortcuts import render
from calorie.forms import FileUploadForm
# Create your views here.


def homePage(request):
    form = FileUploadForm()
    context = {"form": form}
    return render(request, "calorie/index.html", context)
