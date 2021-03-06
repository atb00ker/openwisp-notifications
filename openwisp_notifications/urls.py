from django.urls import include, path

from .api.urls import get_api_urls


def get_urls(api_views=None, social_views=None):
    """
    Returns a list of urlpatterns
    Arguements:
        api_views(optional): views for Notifications API
    """
    urls = [path('api/v1/notifications/', include(get_api_urls(api_views)))]
    return urls


app_name = 'openwisp_notifications'
urlpatterns = get_urls()
