from django.conf import settings
from django.shortcuts import render
from field_scan_app.forms.uload_image_form import ImageUploadForm
from field_scan_app.models import ImageFile
from ml_model_app.views import image_model

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'logged_in/index.html')

def signals(request):
    return render(request, 'logged_in/signals.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['image']
            img = ImageFile.objects.create(
                file=file,
            )

            data = image_model(img.file.name)

            form = ImageUploadForm()
            context = {
                'disease': float(data[0])*100,
                'health': float(data[1])*100,
                'form': form, 
                'uploaded_image_url': '/media/'+img.file.name,
            }

            return render(request, 'logged_in/upload_image.html', context)
        else:
            return render(request, 'logged_in/upload_image.html', {'form': form})
    else:
        form = ImageUploadForm()
        return render(request, 'logged_in/upload_image.html', {'form': form})
