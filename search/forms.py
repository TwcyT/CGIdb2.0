from django import forms


class SearchForm(forms.Form):
    search_type = forms.CharField(label="search_type", max_length=100,required=True)
    filter = forms.CharField(label="filter", max_length=100, required=True)