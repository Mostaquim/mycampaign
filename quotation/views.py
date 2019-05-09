from django.shortcuts import render
from .models import Quotation
from projects.models import Project
from .forms import QuotationForm, QuotationEditForm
from django.views.generic.edit import FormView
from core.views import ModuleView
from django.shortcuts import redirect
# Create your views here.


QUOTATION_MODULE_NAME = "Quotations"


class QuotationFormView(FormView):
    form_class = QuotationForm
    template_name = "quotation/quotation.html"

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)


class QuotationListView(ModuleView):
    client_perm = False
    template_name_admin = "quotation/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = QUOTATION_MODULE_NAME
        context['quotations'] = Quotation.objects.all()
        return context


class QuotationDetailView(ModuleView):
    client_perm = False
    template_name_admin = "quotation/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = QUOTATION_MODULE_NAME
        context['quotation'] = Quotation.objects.get(pk=kwargs['id'])
        return context


class QuotationEditView(ModuleView):
    client_perm = False
    template_name_admin = "quotation/_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = QUOTATION_MODULE_NAME
        context['form'] = QuotationEditForm(
            instance=Quotation.objects.get(pk=kwargs['id']))
        return context

    def post(self, request, *args, **kwargs):
        form = QuotationEditForm(
            request.POST,
            instance=Quotation.objects.get(pk=kwargs['id'])
        )
        if form.is_valid():
            form.save(commit=True)

        return redirect('quotations')


class QuotationGenerateView(ModuleView):
    client_perm = False
    template_name_admin = "quotation/generate.html"

    def post(self, request, *args, **kwargs):
        quotation = Quotation.objects.get(pk=kwargs['id'])
        project = Project.objects.generate(request, quotation)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
