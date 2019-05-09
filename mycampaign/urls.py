"""mycampaign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts import urls as accounturl
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views as dashboard_views
from message.views import MessageEditor
from quotation.views import (
    QuotationFormView,
    QuotationListView,
    QuotationDetailView,
    QuotationGenerateView,
    QuotationEditView
)
from django.contrib.auth.views import LogoutView
from accounts.views import (
    ClientLogin,
    CompanyListView,
    CompanyDetailView,
    resolve_redirect
)

from projects.views import (
    ProjectListView,
    ProjectDetailView,
    ProjectEditView,
    InvoiceListView,
    InvoiceDetailView
)

from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', resolve_redirect),

    path('login/', ClientLogin.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login')),

    path('dashboard/', dashboard_views.Dashboard.as_view(), name='dashboard'),
    path('messages/',  include('message.urls')),

    path('companies/', CompanyListView.as_view(), name='companies'),
    path('companies/<int:id>/', CompanyDetailView.as_view(),
         name='companies_detail'),


    path('quotation/',   QuotationFormView.as_view(), name='order_form'),
    path('quotations/', QuotationListView.as_view(), name='quotations'),
    path('quotations/<int:id>/', QuotationDetailView.as_view(),
         name='quotation_detail'),
    path('quotations/<int:id>/generate/', QuotationGenerateView.as_view()),
    path('quotations/edit/<int:id>/', QuotationEditView.as_view()),

    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='projects'),
    path('projects/edit/<int:id>/', ProjectEditView.as_view()),

    path('invoices/', InvoiceListView.as_view(), name='invoices'),
    path('invoices/<int:id>/',
         InvoiceDetailView.as_view(), name='invoice_detail'),

    path('summernote/', include('django_summernote.urls')),
    url(r'^ajax/', include('core.urls')),
    url(r'^editor-email/(?P<id>.+)/$', MessageEditor.as_view(),
        name='django_summernote-editor-email'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
