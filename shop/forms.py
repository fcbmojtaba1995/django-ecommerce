from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9, initial=1)
