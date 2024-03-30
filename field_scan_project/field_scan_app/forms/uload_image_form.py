from django import forms
from field_scan_app.models import ImageFile

class ImageUploadForm(forms.Form):
    image = forms.FileField(label='', widget=forms.FileInput(attrs={'class': ''}))
    class Meta:
        model = ImageFile
        fields = ['image'] 
