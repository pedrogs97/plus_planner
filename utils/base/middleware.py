"""Project custom middlewares"""
from django.utils.deprecation import MiddlewareMixin

from apps.authenticate.models import Clinic


class CurrentDomainMiddleware(MiddlewareMixin):
    """Custom middleware for get domain"""

    def process_request(self, request):
        """Proccess request to add domain"""
        request.domain = Clinic.objects.get_current(request)
