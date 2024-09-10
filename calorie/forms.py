from django import forms

from calorie.models import Food


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
