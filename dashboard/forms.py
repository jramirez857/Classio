from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label='Please enter the online presentation URL to present to student devices.', max_length=150)

class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=150)
    question = forms.CharField(label='Question', max_length=500)