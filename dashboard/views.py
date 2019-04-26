from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from core.views import ModuleView
# Create your views here.

class Dashboard(ModuleView):
    client_perm = False
    template_name_admin = "dashboard/admin.html"


