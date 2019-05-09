from django.shortcuts import render
from core.views import ModuleView
from .forms import ProjectEditForm
from .models import Project, Invoice
from django.shortcuts import redirect

PROJECT_MODULE_NAME = "Projects"
INVOICE_MODULE_NAME = "Invoices"


class ProjectListView(ModuleView):
    client_perm = False
    template_name_admin = "project/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['module'] = PROJECT_MODULE_NAME
        return context


class ProjectDetailView(ModuleView):
    client_perm = False
    template_name_admin = "project/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = PROJECT_MODULE_NAME
        context['project'] = Project.objects.get(pk=kwargs['id'])
        return context


class ProjectEditView(ModuleView):
    client_perm = False
    template_name_admin = "project/_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = PROJECT_MODULE_NAME
        context['form'] = ProjectEditForm(
            instance=Project.objects.get(pk=kwargs['id']))
        return context

    def post(self, request, *args, **kwargs):
        form = ProjectEditForm(
            request.POST,
            instance=Project.objects.get(pk=kwargs['id'])
        )
        if form.is_valid():
            form.save(commit=True)

        return redirect('projects')


class InvoiceListView(ModuleView):
    client_perm = False
    template_name_admin = "invoice/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoices'] = Invoice.objects.all()
        context['module'] = INVOICE_MODULE_NAME
        return context


class InvoiceDetailView(ModuleView):
    client_perm = False
    template_name_admin = "invoice/detail.html"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['invoice'] = Invoice.objects.get(pk=kwargs['id'])
        context['module'] = INVOICE_MODULE_NAME
        return context
