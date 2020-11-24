from django import forms
from .models import PageInfoModel
from django.utils.translation import gettext_lazy as _

class MyForm(forms.ModelForm):
    class Meta:
        model = PageInfoModel
        fields = [
            "parsed_url",
        ]
        labels = {
            "parsed_url": _('Insert URL to search'),
        }
