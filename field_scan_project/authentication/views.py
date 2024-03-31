
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from authentication.models import UserProfile, Role
from authentication.forms.user_forms import UserProfileForm, UserForm
from authentication.forms.assign_role_form import AssignRoleForm
from authentication.forms.create_edit_form import CreateRoleForm
from authentication.decorators import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView
from authentication.templatetags.auth_tags import user_is_admin
import random
import string

def register(request):
    if request.method == 'GET':
        context = {
            'form_title': 'Добавяне на потребител',
            'btn_text': 'Добави',
        }
        return render(request, 'authentication/user_form.html')
    else:
        f_number = request.POST.get('f_number')
        password = request.POST.get('password')

        user = User.objects.create_user(f_number, password=password)

        profile = UserProfile()
        profile.user = user
        profile.save()

        messages.success(request, 'Потребителят беше добавен успешно!')
        
        return redirect('users')

@login_required(login_url='/auth/signin')
@is_authorized(allowed_roles=['Админ'])
def assign_role(request, id):
    user_profile = UserProfile.objects.get(user_id=id)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            roles = form.cleaned_data['roles']
            user_profile.roles.set(roles)
            if request.user == user_profile.user:
                return redirect('profile')
            else:
                return redirect('users')
    else:
        initial_roles = user_profile.roles.all()
        form = AssignRoleForm(initial={'roles': initial_roles})


    context = {
        'form': form,
        'user_id': id,
    }
    return render(request, "authentication/role/assign_role_form.html", context)

def create_edit_role(request, role):
    if request.method == 'POST':
        form = CreateRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            if role:
                messages.success(request, 'Ролята беше редактирана успешно.')
            else:
                messages.success(request, 'Ролята беше създадена успешно.')
            return redirect('all roles')
        else:
            if role:
                context = {
                    'form': form,
                    'title': 'Редактиране на роля',
                    'button': 'Редактирай',
                }
                return render(request, 'authentication/role/create_edit_role.html', context)
            else:
                context = {
                    'form': form,
                    'title': 'Добавяне на роля',
                    'button': 'Добави',
                }
                return render(request, 'authentication/role/create_edit_role.html', context)
    else:
        form = CreateRoleForm(instance=role)
        
        if role:
            context = {
                'form': form,
                'title': 'Редактиране на роля',
                'button': 'Редактирай',
            }
        else:
            context = {
                'form': form,
                'title': 'Добавяне на роля',
                'button': 'Добави',
            }
        return render(request, 'authentication/role/create_edit_role.html', context)

@login_required(login_url='/auth/signin')
def edit_role(request, pk):
    role = Role.objects.get(pk=pk)
    return create_edit_role(request, role)

def delete_role(request, pk):
    role = Role.objects.get(pk=pk)
    role.delete()
    messages.error(request, 'Ролята беше изтрита успешно!')
    return redirect('all roles')

@login_required(login_url='/auth/signin')
def create_role(request):  
    return create_edit_role(request, None)

@login_required(login_url='/auth/signin')
def all_roles(request):
    roles = Role.objects.all().order_by('name')
    
    context = {
        'roles': roles,
    }

    return render(request, 'authentication/role/all_roles.html', context)

@login_required(login_url='/auth/signin')
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.error(request, 'Потребителят беше изтрит успешно!')
    return redirect('users')

@login_required(login_url='/auth/signin')
def users(request):
    profile = UserProfile.objects.all().order_by('user__first_name', 'user__last_name')

    context = {
        'profiles': profile,
    }
    return render(request, 'authentication/users.html', context)

# TODO: Add validation for createing users with the same usernames/f_numbers
@login_required(login_url='/auth/signin')
@is_authorized(allowed_roles=['Админ'])
def create_user(request):
    if request.method == 'GET':
        context = {
            'form_title': 'Добавяне на потребител',
            'btn_text': 'Добави',
        }
        return render(request, 'authentication/user_form.html', context)
    else:
        f_number = request.POST.get('f_number')
        password = request.POST.get('password')

        user = User.objects.create_user(f_number, password=password)

        profile = UserProfile()
        profile.user = user
        profile.save()

        messages.success(request, 'Потребителят беше добавен успешно!')
        
        return redirect('users')
   
def forgotten_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        print(f'\n\n {request.POST} \n\n')

        try:
            user = get_object_or_404(User, email=email)
            form = PasswordResetForm({'email': user.email})

            if form.is_valid():
                # Generate a new password and reset it for the user
                new_password = User.objects.make_random_password()
                user.set_password(new_password)
                user.save()
            
                html_message = 'Получена е заявка за смяна на паролата на вашият профил в <a href="system.roboclub.bg" style="color:#00acff; fonte-weight:bold;" target="blank">RoboSystem</a> към <a href="roboclub.bg" style="color:#00acff; fonte-weight:bold;" target="blank">RoboClub.bg</a>.<br><br>'+f'Потребител: {user.username}'+f'<br>Нова парола: {new_password}'+'<br><br><br><span style="color:red;">*Ако това не сте били вие, всържете се незабавно с администратор.</span>'
                
                send_mail('Забравена парола', '', 'Admin <administrator@roboclub.bg>', [user.email], html_message=html_message)

                print(f'\n\nOK\n\n')
                messages.success(request, 'Имейлът беше изпратен успешно.')
                return redirect('index')
            
            print(f'\n\nERR\n\n')
            messages.error(request, 'Не беше намерен профил с въведения имейл адрес!')
            return redirect('index')
        except:
            print(f'\n\nERR\n\n')
            messages.error(request, 'Не беше намерен профил с въведения имейл адрес!')
            return redirect('index')
    else:
        form = PasswordResetForm()
        return render(request, 'authentication/forgot_password.html', {'password_form': form})

@login_required(login_url='/auth/signin')
def forgotten_password_by_id(request, id):
    
    try:
        user = get_object_or_404(User, id=id)

        # new_password = User.objects.make_random_password()
        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()
        
        html_message = 'Получена е заявка за смяна на паролата на вашият профил в <a href="system.roboclub.bg" style="color:#00acff; fonte-weight:bold;" target="blank">RoboSystem</a> към <a href="roboclub.bg" style="color:#00acff; fonte-weight:bold;" target="blank">RoboClub.bg</a>.<br><br>'+f'Потребител: {user.username}'+f'<br>Нова парола: {new_password}'+'<br><br><br><span style="color:red;">*Ако това не сте били вие, всържете се незабавно с администратор.</span>'

        
        send_mail('Забравена парола', '', 'System Manager<system@roboclub.bg>', [user.email], html_message=html_message)
        messages.success(request, f'Паролата на потребител с ф.н. {user.username} беше променена успешно.')
    except:
        messages.error(request, 'Възникна грешка при опит за смяна на паролата на потребител с ф.н. {user.username}!!!')
    
    if user_is_admin(user):
        return redirect('users')
    else:
        return redirect('profile')

    # return render(request, 'authentication/create_edit_profile.html', {'password_form': form, 'user': user, 'title': f'Смяна на парола на {user.username}', 'button': 'Изпрати'})

def generate_random_password(length=8):
    characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@login_required(login_url='/auth/signin')
def change_password(request, pk):
    user = User.objects.get(pk=pk)
    
    if request.method == 'GET':
        password_form = PasswordChangeForm(user=user)
        context = {
            'password_form': password_form,
            'title': 'Смяна на паролата',
            'button': 'Запази',
        }
        return render(request, 'authentication/create_edit_profile.html', context)
    
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user,request.POST)
        isIt = password_form.is_valid()
     
        if isIt:
            user = password_form.save()
            update_session_auth_hash(request, user)
           
        print(f"\n\n POST \n {password_form.errors}")

        if password_form.errors:
            for field, errors in password_form.errors.items():
                messages.error(request, f'{field}: {", ".join(errors)}')
        else:
            messages.success(request, 'Профилът беше редактиран успешно!')

        if request.user == user:
            return redirect('profile')
        else:
            return redirect('users')

@login_required(login_url='/auth/signin')
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    profile_form = UserProfileForm(instance=user.userprofile)

    if request.method == 'GET':
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Редактиране на профила',
            'button': 'Редактирай',
        }
        return render(request, 'authentication/create_edit_profile.html', context)
    else:
        user_form = UserForm(request.POST, instance=user)
        user_form.save()
        profile_form = UserProfileForm(request.POST, instance=user.userprofile)
        profile_form.save()

        messages.success(request, 'Профилът беше редактиран успешно!')

        if request.user == user:
            return redirect('profile')
        else:
            return redirect('users')

@login_required(login_url='/auth/signin')
def profile(request):
    profile = request.user.userprofile

    if not profile:
        profile = UserProfile()
        profile.user = request.user
        profile.save()
        
    print(f'\n\n\n{profile.roles.exists()}\n\n\n')

    context = {
        'profile': profile
    }

    return render(request, 'authentication/user_profile.html', context)

@login_required(login_url='/auth/signin')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('dashboard')

    return redirect('main index')
    
def signin(request):
    # try:
    if request.user.is_authenticated:
    #     print('\n\n auth \n\n')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = User.objects.get(username=username)

        if not user:
            context = {
                'err_msg':'Error while logging in!',
            }
            return render(request, 'authentication/signin.html', context)
        
        user = authenticate(username = user.username, password = password)

        if not user:
            context = {
                'err_msg':'Error while logging in!',
            }
            return render(request, 'authentication/signin.html', context)

        login(request, user)

        if remember_me:
            request.session.set_expiry(30 * 24 * 60 * 60)

        return redirect('dashboard')
        
    return render(request, 'authentication/signin.html')

    # except Exception as e:
    #     print('\n\n err \n\n')
    #     print(e)

def not_authorized(request):
    return render(request,'authentication/not_authorized.html')