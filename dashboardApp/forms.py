from django import forms
from .models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes 
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'

    
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due_date':DateInput()}
        fields = ['subject','title','description','due_date','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200,label='Search for content: ')


