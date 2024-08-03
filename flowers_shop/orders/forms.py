from django import forms
from django.contrib.auth import get_user_model  # Импортируйте get_user_model для получения пользовательской модели

User = get_user_model()

class OrderForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    address = forms.CharField(label='Адрес доставки', max_length=255)
    phone = forms.CharField(label='Телефон', max_length=20)
    comments = forms.CharField(label='Комментарии', widget=forms.Textarea, required=False)
