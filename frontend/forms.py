from django import forms


class IdentifyForm(forms.Form):
    image = forms.ImageField()