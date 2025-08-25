from dashboard.models import Notification

def default(request):
    if request.user.is_authenticated:
        all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        all_notifications = []
        unread_count = 0

    return {
        'notifications': all_notifications,
        'unread_count': unread_count,
    }
