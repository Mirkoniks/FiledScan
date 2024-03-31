from django import template
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from authentication.models import UserProfile, Role
from field_scan_app.models import Signal

register = template.Library()

def is_user_authenticated(user):
    return user.is_authenticated

def user_is_admin(user):
    r = Role.objects.get(name='Админ')

    roles = user.userprofile.roles.all()

    return r in roles

def user_is_club_member(user):
    r = Role.objects.get(name='Член на клуба')

    roles = user.userprofile.roles.all()

    return r in roles

def user_is_us_member(user):
    access_roles = ['Админ', 'Член на УС']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def get_user_names(user):
    return f'{user.first_name} {user.last_name}'

def get_user_roles(user):
    roles = list(user.userprofile.roles.values_list('name', flat=True))
    return '| '.join(roles)

def user_is_only_in_student_council(user):
    try:
        r = Role.objects.get(name='Член на Студентски съвет')

        roles = user.userprofile.roles.all()

        if roles.__len__() == 1 and r in roles:
            return True
        else:
            return False
    except:
        return False

def user_is_in_student_council(user):
    r = Role.objects.get(name='Член на Студентски съвет')

    roles = user.userprofile.roles.all()

    return r in roles

def user_can_create_edit_protocol(user):
    access_roles = ['Админ', 'Председател', 'Протоколчик', 'Член на УС', 'Член на клуба']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_assept_protocol(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_delete_protocol(user):
    access_roles = ['Админ', 'Председател', 'Протоколчик']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_see_users(user):
    access_roles = ['Админ', 'Председател', 'Протоколчик']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_access_roles(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_access_users(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_create_edit_users(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_assign_roles(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    
    return roles.exists()

def user_can_create_edit_inventory(user):
    access_roles = ['Админ', 'Председател', 'Протоколчик']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_approve_inventory(user):
    access_roles = ['Админ', 'Председател']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()

def user_can_edit_docs(user):
    access_roles = ['Админ', 'Председател', 'Член на УС']
    roles = user.userprofile.roles.all().filter(
        Q(name__in=access_roles)
    )
    return roles.exists()
    user_activity = UserActivity.objects.get(user=user)
    if user_activity:
        time_in_minutes = (timezone.now() - user_activity.timestamp).total_seconds()/60

        if time_in_minutes > 60:
            if time_in_minutes/60 > 24:
                if time_in_minutes/60/24 > 7:
                    return f'Последна ктивност {int(time_in_minutes/60/24/7)} седм.'
                else:
                    return f'Последна ктивност {int(time_in_minutes/60/24)} дни.'
            else:
                return f'Последна ктивност {int(time_in_minutes/60)} ч.'
        elif time_in_minutes >= 1:
            return f'Последна ктивност {int(time_in_minutes)} мин.'
        elif time_in_minutes < 1:
            return f'Последна ктивност {int(time_in_minutes*60)} сек.'
        else:
            return 'transparent'
    else:
        return 'transparent'

def last_two_signals():
    data = list(Signal.objects.all()[:-2])
    print(f'\n\n{data}\n\n')
    return data

register.filter('is_user_authenticated', is_user_authenticated)
register.filter('user_is_admin', user_is_admin)
register.filter('user_is_club_member', user_is_club_member)
register.filter('user_is_us_member', user_is_us_member)
register.filter('get_user_names', get_user_names)
register.filter('get_user_roles', get_user_roles)
register.filter('user_is_in_student_council', user_is_in_student_council)
register.filter('user_is_only_in_student_council', user_is_only_in_student_council)
register.filter('user_can_create_edit_protocol', user_can_create_edit_protocol)
register.filter('user_can_assept_protocol', user_can_assept_protocol)
register.filter('user_can_delete_protocol', user_can_delete_protocol)
register.filter('user_can_access_roles', user_can_access_roles)
register.filter('user_can_access_users', user_can_access_users)
register.filter('user_can_create_edit_users', user_can_create_edit_users)
register.filter('user_can_assign_roles', user_can_assign_roles)
register.filter('user_can_create_edit_inventory', user_can_create_edit_inventory)
register.filter('user_can_approve_inventory', user_can_approve_inventory)
register.filter('user_can_edit_docs', user_can_edit_docs)
register.filter('last_two_signals', last_two_signals)