from .models import Project
from django import forms


class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'company',
            'progress',
            'type_of_service',
            'quantity_of_flyers',
            'number_of_boxes',
            'type_of_service',
            'campaign_start_date',
            'campaign_finish_date',
            'status',
            'priority'
        ]
