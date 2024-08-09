# analytics/forms.py

from django import forms
from main.models import Tovar

class TovarForm(forms.ModelForm):
    class Meta:
        model = Tovar
        fields = [
            'Nazvanie',
            'Cena',
            'Img_url',
            'Opisanie',
            'ID_TipTovara',
            'ID_KategorTovara',
            'Reiting',
            'kolich_otzyv'
        ]
        labels = {
            'Nazvanie': 'Название товара',
            'Cena': 'Цена (руб.)',
            'Img_url': 'URL изображения',
            'Opisanie': 'Описание товара',
            'ID_TipTovara': 'Тип товара',
            'ID_KategorTovara': 'Категория товара',
            'Reiting': 'Рейтинг товара',
            'kolich_otzyv': 'Количество отзывов'
        }
        widgets = {
            'Nazvanie': forms.TextInput(attrs={'class': 'form-control'}),
            'Cena': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'Img_url': forms.URLInput(attrs={'class': 'form-control', 'required': False}),
            'Opisanie': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'ID_TipTovara': forms.Select(attrs={'class': 'form-control'}),
            'ID_KategorTovara': forms.Select(attrs={'class': 'form-control'}),
            'Reiting': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'kolich_otzyv': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super(TovarForm, self).__init__(*args, **kwargs)
        self.fields['Img_url'].required = False  # Поле не обязательно к заполнению
