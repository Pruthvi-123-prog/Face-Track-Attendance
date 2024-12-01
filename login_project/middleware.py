from django.shortcuts import redirect
from django.urls import reverse

class DataAccessMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        public_paths = [
            '/login/',
            '/signup/',
            '/home/',
            '/admin/',
            '/',
            '/data/verify/'
        ]

        if request.path in public_paths:
            return self.get_response(request)

        if request.path.startswith('/data/'):
            if not request.session.get('data_access_verified'):
                return redirect('verify_data_access')

        return self.get_response(request)