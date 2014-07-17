from django import forms
from .models import Stock
from smirik.apps.smirik_auth.forms import UserFormMixin

class StockForm(forms.ModelForm, UserFormMixin):
    """class for managing creation and updating of stocks."""
    class Meta:
        model = Stock
        fields = ['name']
