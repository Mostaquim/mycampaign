from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect, resolve_url
from core.views import ModuleView
from .models import Company
# Create your views here.
COMPANY_MODULE_NAME = 'Companies'


class ClientLogin(LoginView):
    def __init__(self, *args, **kwargs):
        self.template_name = 'accounts/login.html'
        return super().__init__(*args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_staff:
            return resolve_url('dashboard')
        else:
            return resolve_url('a')


class CompanyListView(ModuleView):

    client_perm = False
    template_name_admin = "accounts/company_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = COMPANY_MODULE_NAME
        context['companies'] = Company.objects.all()
        return context


class CompanyDetailView(ModuleView):
    client_perm = False
    template_name_admin = "accounts/company_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = COMPANY_MODULE_NAME
        context['company'] = Company.objects.get(pk=kwargs['id'])
        return context


def resolve_redirect(request):
    if request.user.is_staff:
        return redirect('dashboard')
    elif request.user.is_client:
        return redirect('projects')
    else:
        return redirect('login')
