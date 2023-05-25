from django import forms

class MP3UploadForm(forms.Form):
    mp3_file = forms.FileField(label='Select an MP3 file')