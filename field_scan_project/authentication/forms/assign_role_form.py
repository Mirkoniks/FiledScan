from django import forms
from authentication.models import Role

class AssignRoleForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label='Роли',
        required=False,
        )

    class Meta:
        model = Role
        fields = ['roles']
    
    
