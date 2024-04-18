from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=120,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter fullname"}
        ),
    )
    born_date = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    born_location = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class TagForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter name"}
        ),
    )

    class Meta:
        model = Tag
        fields = ["name"]



class QuoteForm(forms.ModelForm):
    quote = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Enter quote"}
        ),
    )
    author = forms.IntegerField(widget=forms.Select())


    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "author"]
