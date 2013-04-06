from django import forms
from models import Survey
from django.core.exceptions import ValidationError

#class SurveyForm(forms.ModelForm):
#    """
#        Provides a Form for creating/editing a Survey
#    """
#    class Meta:
#        model = Survey
#    
    
class SurveyForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea(), required=True)
    
    
    def clean_title(self):
        data = self.cleaned_data
        
        title = data["title"]
        
        if Survey.objects.filter(title = title).exists():
            raise ValidationError("title already taken")
        
        return data