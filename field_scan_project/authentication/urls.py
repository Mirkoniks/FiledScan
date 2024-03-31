from django.urls import path, include
from authentication.views import *

urlpatterns = [
    path('signin', signin, name='signin'),
    path('logout', user_logout, name='logout'),
    path('register', register, name="register"),

    # user
    path('profile', profile, name='profile'),
    path('users', users, name="users"),
    path('create-user', create_user, name="create user"),
    path('delete-user/<int:pk>', delete_user, name="delete user"),

    path('assign-role/<int:id>', assign_role, name='assign role'),
    path('edit-profile/<int:pk>', edit_profile, name='edit profile'),
    path('change-password/<int:pk>', change_password, name='change password'),
    path('forgotten-password', forgotten_password, name='forgotten password'),
    path('forgotten-password-by-id/<int:id>', forgotten_password_by_id, name='forgotten password by id'),

    path('roles-all', all_roles, name="all roles"),
    path('create-role', create_role, name="create role"),
    path('edit-role/<int:pk>', edit_role, name="edit role"),
    path('delete-role/<int:pk>', delete_role, name="delete role"),
    path('not-authorized',not_authorized,name="not authorized")
]
