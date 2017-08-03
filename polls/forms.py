from django import forms
from .models import Poll, Choice
from datetime import datetime


class QuestionForm(forms.ModelForm):
    pub_date = forms.DateTimeField(widget=forms.HiddenInput(), initial = datetime.now())

    class Meta:
        model = Poll
        fields = "__all__"

class ChoiceForm(forms.ModelForm):
    votes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Choice
        fields = "__all__"
