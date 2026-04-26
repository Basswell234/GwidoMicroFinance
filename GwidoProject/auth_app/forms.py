"""
Auth App Forms
This module contains Django forms for user registration and authentication.
"""

from django import forms
from django.contrib.auth.models import User
from village_banking.models import Person
import re


class RegistrationForm(forms.Form):
    """
    Comprehensive registration form that combines User and Person model fields.
    Allows users to create an account with personal information.
    """
    
    # User model fields
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter a unique username',
            'autocomplete': 'username'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )
    
    password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter a strong password (min 8 characters)',
            'autocomplete': 'new-password'
        })
    )
    
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        })
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your first name',
            'autocomplete': 'given-name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your last name',
            'autocomplete': 'family-name'
        })
    )
    
    # Person model fields
    sex = forms.ChoiceField(
        choices=Person.SEX_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg'
        })
    )
    
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your address',
            'autocomplete': 'street-address'
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your phone number',
            'autocomplete': 'tel'
        })
    )
    
    occupation = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your occupation',
        })
    )
    
    nrc = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your National Registration Certificate number',
        }),
        label='NRC (National Registration Certificate)'
    )
    
    # Optionals
    membership_desc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter any additional membership information (optional)',
            'rows': 3
        }),
        label='Membership Description (Optional)'
    )
    
    def clean_username(self):
        """Validate that username is unique"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        return username
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered. Please use a different email or login.')
        return email
    
    def clean_password(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise forms.ValidationError('Password must contain at least one number.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        
        return password
    
    def clean_phone_number(self):
        """Validate phone number format"""
        phone_number = self.cleaned_data.get('phone_number')
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)\.]+', '', phone_number)
        if not cleaned.isdigit() or len(cleaned) < 7:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone_number
    
    def clean(self):
        """Validate that passwords match"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match. Please try again.')
        
        return cleaned_data
