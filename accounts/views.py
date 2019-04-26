from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import resolve_url
# Create your views here.

class ClientLogin(LoginView):
    def __init__(self, *args, **kwargs):
        self.template_name= 'accounts/login.html'
        return super().__init__(*args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_staff:
            return resolve_url('dashboard')
        else:
            return resolve_url('a')
