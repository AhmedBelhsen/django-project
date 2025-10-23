from django import forms
from .models import Conference


class conference_form(forms.ModelForm):
    class Meta:
        model=Conference
        fields=["name","theme","start_date","end_date","location","description"]
        labels={
            "name":"Nom de la conférence",
            "theme":"Thème",
            "start_date":"Date de début",
            "end_date":"Date de fin",
            "location":"Lieu",
            "description":"Description",
        }
        widgets={
            "name":forms.TextInput(attrs={"placeholder":"Nom de la conférence Ex: AI Conference 2024"}),
            "start_date":forms.DateInput(attrs={"type":"date","placeholder":"date de début"}),
            "end_date":forms.DateInput(attrs={"type":"date","placeholder":"date de fin"})
        }