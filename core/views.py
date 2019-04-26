from django.views.generic.base import View, ContextMixin
from django.core.exceptions import ImproperlyConfigured,  PermissionDenied
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
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
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [template]


class ModuleView(ClientAdminMixin, ContextMixin, ProtectedView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
