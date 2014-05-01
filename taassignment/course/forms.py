from django import forms

class ErrorForm(forms.Form):
    msg = forms.CharField(max_length=1)

class UploadFileForm(forms.Form):
    file  = forms.FileField()
