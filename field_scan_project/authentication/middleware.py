from django.utils import timezone
from authentication.models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                user_activity = UserActivity.objects.get(user=request.user)
                user_activity.timestamp=timezone.now()
                user_activity.save()
            except:
                UserActivity.objects.create(user=request.user, timestamp=timezone.now())

        return response
