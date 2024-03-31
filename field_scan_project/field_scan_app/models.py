from django.db import models

def project_blank_file_path(instance, filename):
    project_number = instance.project.id
    subfolder = f'project_blanks/{project_number:04d}.pdf'
    return subfolder

class ImageFile(models.Model):
    file = models.FileField()

class Signal(models.Model):
    image = models.ForeignKey(ImageFile, on_delete=models.CASCADE)
    disease = models.FloatField()
    health = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
