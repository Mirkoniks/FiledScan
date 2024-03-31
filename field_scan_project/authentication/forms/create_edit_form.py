from django import forms
from authentication.models import Role

class CreateRoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        labels = {
            'name': 'Име на ролята',
        }