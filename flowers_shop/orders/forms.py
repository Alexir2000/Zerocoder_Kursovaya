from django import forms
from main.models import Users

class OrderForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.HiddenInput())
    address = forms.CharField(label='Адрес доставки', max_length=255)
    phone = forms.CharField(label='Телефон', max_length=20)
    comments = forms.CharField(label='Комментарии', widget=forms.Textarea, required=False)
