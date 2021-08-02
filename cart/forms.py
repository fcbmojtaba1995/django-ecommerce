from django import forms


class RemoveFormCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9, initial=1)
