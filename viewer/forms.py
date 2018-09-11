from django import forms


class SearchForm(forms.Form):
    target = forms.CharField(label='', required=False)
