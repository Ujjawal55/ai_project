from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(label="Select a file")

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
