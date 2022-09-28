from django import forms

from evaluation_manager.models import EvaluationManager


class EvaluationManagerForm(forms.ModelForm):
    class Meta:
        model = EvaluationManager
        fields = "__all__"
        exclude = ("archived",)

        widgets = {
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }