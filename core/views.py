from django.views.generic.base import View, ContextMixin
from django.core.exceptions import ImproperlyConfigured,  PermissionDenied
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from .models import Postcodes
from json import dumps
from django.utils.datastructures import MultiValueDictKeyError
from .allowed import MIME_TYPES, MAX_UPLOAD_SIZE
from .models import Attachments
# Create your views here.


class ProtectedView(AccessMixin, View):
    client_perm = None
    login_url = '/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not self.client_perm:
            if not request.user.is_staff:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ClientAdminMixin:
    """A mixin that can be used to render a template."""
    template_name_admin = None
    template_name_client = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if self.request.user.is_staff:
            template = self.template_name_admin
        else:
            template = self.template_name_client

        if template is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of "
                " 'get_template_names()'")
        else:
            return [template]


class ModuleView(ClientAdminMixin, ContextMixin, ProtectedView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def get_postcodes(request):
    query_json = []
    if request.GET.get('q'):
        slug = request.GET['q']
        query = Postcodes.objects.filter(full_name__istartswith=slug)[:3]

        for q in query:
            ar = {
                'id': q.pk,
                'text': q.area + q.district + " " +
                q.sector + " - " + q.locality + " (" + q.total + ")"
            }
            query_json.append(ar)

    query_json = {
        'items': query_json,
        'more': False
    }

    return HttpResponse(dumps(query_json))


def file_upload(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.FILES['file'].name
        size = request.FILES['file'].size
        mime = request.FILES['file'].content_type
        print("%s %s %s" % (name, size, mime))
        if size > MAX_UPLOAD_SIZE:
            return HttpResponse("Filze Size Exceeded", status=403)
        if mime in MIME_TYPES:
            attachments = Attachments(
                name=name,
                attachment=request.FILES['file']
            )
            attachments.save()
            return HttpResponse(attachments.pk)
    return HttpResponse("Invalid File Type", status=403)
