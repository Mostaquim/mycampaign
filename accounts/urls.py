from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.ClientLogin.as_view(), name='login'),
    # path('logout', views.login, name='logout'),
    path('logout', LogoutView.as_view(next_page='login'))
]