from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidgetBase
from .models import Messages
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import json


class SummernoteWidgetEmailAdmin(SummernoteWidgetBase):
    def render(self, name, value, attrs=None, **kwargs):
        summernote_settings = self.summernote_settings()
        summernote_settings.update(self.attrs.get('summernote', {}))

        html = super(SummernoteWidgetEmailAdmin, self).render(
            name, value, attrs=attrs, **kwargs
        )
        context = {
            'id': attrs['id'].replace('-', '_'),
            'id_src': attrs['id'],
            'flat_attrs': flatatt(self.final_attr(attrs)),
            'settings': json.dumps(summernote_settings),
            'src': reverse('django_summernote-editor-email',
                           kwargs={'id': attrs['id']}),

            # Width and height have to be pulled out to create an iframe with
            # correct size
            'width': summernote_settings['width'],
            'height': summernote_settings['height'],
        }

        html += render_to_string('widgets/summernote_email.html', context)
        return mark_safe(html)


class MessageForm(ModelForm):
    # subject = forms.CharField()
    # text = forms.CharField(widget=SummernoteWidgetEmailAdmin())
    class Meta:
        model = Messages
        fields = ['reciever', 'message', 'subject']
        widgets = {
            'message': SummernoteWidgetEmailAdmin()
        }
