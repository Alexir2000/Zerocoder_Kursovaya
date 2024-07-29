

from django import forms

from main.models import Tip_Tovara, Kat_Tovara


class TovarSearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=255, required=False)
    category = forms.ChoiceField(label='Категория', required=False)
    type = forms.ChoiceField(label='Тип', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(None, 'Все категории')] + [(cat.ID, cat.Kategoriya) for cat in Kat_Tovara.objects.all()]
        self.fields['type'].choices = [(None, 'Все типы')] + [(typ.ID, typ.Tip) for typ in Tip_Tovara.objects.all()]
