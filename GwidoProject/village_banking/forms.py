"""
Village Banking Forms
This module contains Django forms for the village banking application.
"""

from django import forms
from .models import Investment


class InvestmentForm(forms.ModelForm):
    """
    Form for creating and updating investment records.
    Includes fields for membership, date, investment amount, category, penalty, and expected date.
    """
    
    class Meta:
        model = Investment
        fields = ['date', 'investment_amount', 'category', 'penalty', 'expected_date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg',
                'placeholder': 'Select Investment Date'
            }),
            'investment_amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Investment Amount',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'penalty': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Penalty Amount',
                'step': '0.01',
                'min': '0'
            }),
            'expected_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg',
                'placeholder': 'Select Expected Completion Date'
            }),
        }
        labels = {
            'date': 'Investment Date',
            'investment_amount': 'Investment Amount',
            'category': 'Investment Category',
            'penalty': 'Penalty Amount',
            'expected_date': 'Expected Completion Date',
        }
