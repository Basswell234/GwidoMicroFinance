"""
Village Banking Forms
This module contains Django forms for the village banking application.
"""

from django import forms
from .models import Investment, Loan


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


class LoanRequestForm(forms.ModelForm):
    """
    Form for requesting a loan.
    Automatically assigns membership from the logged-in user.
    Issue date is set to today and due date is automatically set to 3 months later.
    Required fields: amount. Optional: collateral_desc.
    """
    
    class Meta:
        model = Loan
        fields = ['amount', 'collateral_desc']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Loan Amount',
                'step': '0.01',
                'min': '100',
                'required': True
            }),
            'collateral_desc': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Describe the collateral you will provide (optional)',
                'rows': 4,
                'required': False
            }),
        }
        labels = {
            'amount': 'Loan Amount',
            'collateral_desc': 'Collateral Description (Optional)',
        }
    
    def clean_amount(self):
        """Validate loan amount"""
        amount = self.cleaned_data.get('amount')
        if amount and amount < 100:
            raise forms.ValidationError('Loan amount must be at least 100.')
        return amount
