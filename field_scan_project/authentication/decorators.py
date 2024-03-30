from functools import wraps
from django.shortcuts import redirect,render
from django.contrib import messages

def is_authorized(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and any(role.name in allowed_roles for role in request.user.userprofile.roles.all()):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Нямате право на достъп до тази страница.")
                return render(request,'authentication/not_authorized.html')  
        return wrapper
    return decorator