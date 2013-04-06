from django import forms
from models import Survey


class SurveyForm(forms.ModelForm):
    """
        Provides a Form for creating/editing a Survey
    """
    class Meta:
        model = Survey
    
    
class SurveyForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea(), required=True)
    