# flowers_shop/catalog/forms.py

from django import forms
from main.models import Tip_Tovara, Kat_Tovara, BaseOtziv

class TovarSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск')
    category = forms.ModelChoiceField(queryset=Kat_Tovara.objects.all(), required=False, label='Категория')
    type = forms.ModelChoiceField(queryset=Tip_Tovara.objects.all(), required=False, label='Тип товара')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(None, 'Все категории')] + [(cat.ID, cat.Kategoriya) for cat in Kat_Tovara.objects.all()]
        self.fields['type'].choices = [(None, 'Все типы')] + [(typ.ID, typ.Tip) for typ in Tip_Tovara.objects.all()]

class AddReviewForm(forms.Form):
    reiting = forms.IntegerField(label='Рейтинг', min_value=1, max_value=5, initial=5)
    otzyv = forms.CharField(
        label='Отзыв',
        widget=forms.Textarea(attrs={'rows': 4})
    )
