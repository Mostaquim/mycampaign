from django.shortcuts import render
from .forms import MessageForm
from core.views import ModuleView
# Create your views here.

class Main(ModuleView):
    client_perm = True
    template_name_admin = "messages/admin_main.html"

def send_message(request):
    form = MessageForm()
    return render(request, 'messages/_send_message.html', {'form': form})