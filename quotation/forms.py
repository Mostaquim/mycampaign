from django import forms
from .models import Quotation, Format, GSM
from core.models import Postcodes, Attachments
from .choices import *
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from accounts.models import User


class AutyRadio(forms.RadioSelect):
    template_name = 'widgets/auty_radio.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)


class GSMSelect(forms.RadioSelect):
    template_name = 'widgets/gsm_select_widget.html'

    def get_allowed_formats(self, value):
        gsm = GSM.objects.get(pk=value)
        formats = gsm.allowed_format.all()
        return_format = []
        for f in formats:
            return_format.append(str(f.pk))
        return ','.join(return_format)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        optgroups = context['widget']['optgroups']

        for i in range(len(optgroups)):
            try:
                allowed_format = self.get_allowed_formats(
                    optgroups[i][1][0]['value'])
                optgroups[i][1][0]['attrs']['data-formats'] = allowed_format
            except:
                print('')
        context['widget']['optgroups'] = optgroups
        return render_to_string(self.template_name, context)


class QuotationForm(forms.Form):
    type_of_service = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=AutyRadio,
        initial=SERVICE_CHOICES[0]
    )
    number_of_boxes = forms.ChoiceField(
        choices=BOX_TO_COLLECT,
        widget=AutyRadio,
        initial=BOX_TO_COLLECT[0]
    )
    type_of_media = forms.ChoiceField(
        choices=TYPE_OF_MEDIA,
        widget=AutyRadio,
        initial=TYPE_OF_MEDIA[0]
    )
    require_collection = forms.ChoiceField(
        choices=REQUIRE_COLLECTION,
        widget=AutyRadio,
        initial=REQUIRE_COLLECTION[0]
    )
    quantity_of_flyers = forms.CharField(widget=forms.NumberInput)
    title_of_media = forms.CharField()
    campaign_details = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5})
    )
    business_name = forms.CharField()
    full_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    postcode = forms.CharField()
    agreed_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, required=True)
    target_postcodes = forms.ModelMultipleChoiceField(
        queryset=Postcodes.objects.all()
    )
    campaign_start_date = forms.DateField()
    campaign_finish_date = forms.DateField()
    special_instruction = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5})
    )
    account_manager = forms.ModelChoiceField(
        queryset=User.objects.filter(accountant=True),
        required=False
    )
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    printing_required = forms.BooleanField(required=False)
    pages = forms.ChoiceField(choices=PAGES, required=False)
    page_orientation = forms.ChoiceField(
        choices=PAGE_ORIENTATION, required=False)
    page_format = forms.ModelChoiceField(
        queryset=Format.objects.all(),
        initial=1,
        required=False
    )
    gsm = forms.ModelChoiceField(
        queryset=GSM.objects.all(),
        widget=GSMSelect,
        initial=1,
        required=False
    )
    colours = forms.ChoiceField(choices=COLORS, required=False)
    processing = forms.ChoiceField(choices=PROCESSING, required=False)
    attachments = forms.ModelMultipleChoiceField(
        queryset=Attachments.objects.all(),
        required=False
    )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise forms.ValidationError("Passwords does not match")
        return confirm_password

    def save(self, request, commit=True):
        data = self.cleaned_data

        obj = Quotation()

        obj.type_of_service = data['type_of_service']
        obj.type_of_media = data['type_of_media']
        obj.require_collection = data['require_collection']
        obj.quantity_of_flyers = data['quantity_of_flyers']
        obj.title_of_media = data['title_of_media']
        obj.campaign_details = data['campaign_details']

        obj.business_name = data['business_name']
        obj.full_name = data['full_name']
        obj.email = data['email']
        obj.phone = data['phone']
        obj.street = data['street']
        obj.city = data['city']
        obj.postcode = data['postcode']

        obj.agreed_cost = data['agreed_cost']
        obj.campaign_start_date = data['campaign_start_date']
        obj.campaign_finish_date = data['campaign_finish_date']
        obj.special_instruction = data['special_instruction']
        obj.account_manager = data['account_manager']

        obj.save()
        for postcode in data['target_postcodes']:
            obj.target_postcodes.add(postcode)
        for attachments in data['attachments']:
            obj.attachments.add(attachments)
        obj.save()


class QuotationEditForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'status',
            'assigned_user'
        ]
