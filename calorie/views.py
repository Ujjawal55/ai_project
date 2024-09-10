from django.shortcuts import render, redirect
from calorie.forms import FileUploadForm
from calorie.models import Food
from calorie.utils import getContent


def upload_view(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.name = (file.image.name).split(".")[0]
            file.save()
            return redirect("result", file_name=file.name)
        else:
            print("form is not valid")

    else:
        form = FileUploadForm()
    context = {"form": form}
    return render(request, "calorie/index.html", context)


def result_view(request, file_name):
    page = "result"
    items = getContent(file_name)
    file = Food.objects.get(name=file_name)  # type:ignore
    context = {"page": page, "file": file, "items": items}
    return render(request, "calorie/index.html", context)
