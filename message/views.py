from django.shortcuts import render
from .forms import MessageForm
from core.views import ModuleView
from django_summernote.utils import using_config
from django.contrib.staticfiles.templatetags.staticfiles import static
from django_summernote.views import SummernoteEditor
from django.http import HttpResponseRedirect, HttpResponse

class Main(ModuleView):
    client_perm = True
    template_name_admin = "messages/admin_main.html"

def send_message(request):
    form = MessageForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form =  MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return HttpResponseRedirect('/messages/')

    return render(request, 'messages/_send_message.html', {'form': form})

class MessageEditor(SummernoteEditor):
    template_name = 'widgets/summernote_iframe.html'