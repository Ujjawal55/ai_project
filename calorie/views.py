from django.shortcuts import render, redirect
from calorie.forms import FileUploadForm
from django.core.files.storage import default_storage

# TODO: add the handle when the image that is uploaded is not valid..


def upload_view(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_name = default_storage.save(uploaded_file.name, uploaded_file)
            return redirect("result", file_name=file_name)

    else:
        form = FileUploadForm()
        context = {"form": form}
        return render(request, "calorie/index.html", context)


def result_view(request, file_name):
    page = "result"
    context = {"page": page, "file_name": file_name}
    return render(request, "calorie/index.html", context)
