from django import forms
from flowers_shop.main.models import BaseOtziv, Tovar

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BaseOtziv
        fields = ['ID_Tovar', 'Otziv', 'ReitingTovara']
        widgets = {
            'ID_Tovar': forms.HiddenInput(),
            'Otziv': forms.Textarea(attrs={'rows': 4}),
            'ReitingTovara': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }
