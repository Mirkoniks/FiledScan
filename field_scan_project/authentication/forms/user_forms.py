from django import forms
from django.contrib.auth.models import User
from authentication.models import UserProfile, Role


class AddRoleToUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    role = forms.ModelChoiceField(queryset=Role.objects.all())

    class Meta:
        model = UserProfile
        fields = ('roles', 'role', )
        labels = {
            'roles': 'Роли',
            'role': 'Роля',
        }
        
    def save(self):
        user = self.cleaned_data['user']
        role = self.cleaned_data['role']
        user.userprofile.roles.add(role)



class CreateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # class Meta:
    #     model = User

    # f_number = forms.CharField(
    #     label='Ф. Номер',
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': 'Ф. Номер',
    #             # 'onchange': 'formIsValid()',
    #         }
    #     )
    # )

    # password = forms.CharField(
    #     label = 'Парола',
    #     widget = forms.PasswordInput(
    #         attrs={
    #             'placeholder': 'Парола',
    #         }
    #     )
    # )

    # rep_password = forms.CharField(
    #     label = 'Повторете паролата',
    #     widget = forms.PasswordInput(
    #         attrs={
    #             'placeholder': 'Повторете паролата',
    #         }
    #     )
    # )
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     for (_, field) in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    # password = forms.CharField(
    #     widget = forms.PasswordInput()
    # )

    # class Meta:
    #     model = User
    #     model = User
    #     fields = ('username', 'first_name', 'last_name', 'email', 'password')
    #     labels = {
    #         'username': 'Фак. номер',
    #         'first_name': 'Име',
    #         'last_name': 'Фамилия',
    #         'email': 'Имейл',
    #         'password': 'Парола',
    #     }

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' )
        labels = {
            'username': 'Ф. Номер',
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'email': 'Имейл',
        }


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserProfile
        fields = ('university', 'faculty')
        labels = {
            'university': 'Университет',
            'faculty': 'Факултет',
        }
