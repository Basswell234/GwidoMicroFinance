"""
Village Banking Views
This module contains views for handling investment, transaction, loan, and other
financial operations in the village banking application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment, Membership, Person, Loan
from .forms import InvestmentForm, LoanRequestForm
from datetime import date, timedelta


@login_required
def investment(request):
    """
    Handle investment form submission and display.
    Automatically retrieves the membership of the logged-in user.
    GET: Display the investment form
    POST: Process and save investment data with automatic membership assignment
    """
    # Get the Person associated with the logged-in user
    try:
        person = Person.objects.get(user=request.user)
        membership = Membership.objects.get(person_id=person)
    except (Person.DoesNotExist, Membership.DoesNotExist):
        messages.error(request, 'You must have a valid membership to record investments.')
        return redirect('home')
    
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            # Create the investment with the auto-populated membership
            investment_obj = form.save(commit=False)
            investment_obj.membership_id = membership
            investment_obj.save()
            messages.success(request, 'Investment recorded successfully!')
            return redirect('investment')
        else:
            messages.error(request, 'There was an error in your form. Please check and try again.')
    else:
        form = InvestmentForm()
    
    context = {
        'form': form,
        'membership': membership,
        'person': person
    }
    return render(request, 'village_banking/investment.html', context)


@login_required
def request_loan(request):
    """
    Handle loan request form submission and display.
    Automatically retrieves the membership of the logged-in user.
    Issue date is set to today and due date is automatically set to 3 months from today.
    GET: Display the loan request form
    POST: Process and save loan request with automatic membership assignment and pending status
    """
    # Get the Person associated with the logged-in user
    try:
        person = Person.objects.get(user=request.user)
        membership = Membership.objects.get(person_id=person)
    except (Person.DoesNotExist, Membership.DoesNotExist):
        messages.error(request, 'You must have a valid membership to request loans.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            # Create the loan with the auto-populated membership and default values
            loan_obj = form.save(commit=False)
            loan_obj.membership_id = membership
            loan_obj.loan_status = 'pending'
            loan_obj.amount_remaining = form.cleaned_data['amount']  # Initially equals the full amount
            loan_obj.loan_issue_date = date.today()  # Set to today
            loan_obj.due_date = date.today() + timedelta(days=90)  # 3 months from today
            loan_obj.save()
            messages.success(request, 'Loan request submitted successfully! Our team will review your request shortly.')
            return redirect('request_loan')
        else:
            messages.error(request, 'There was an error in your form. Please check and try again.')
    else:
        form = LoanRequestForm()
    
    context = {
        'form': form,
        'membership': membership,
        'person': person,
        'today': date.today(),
        'due_date': date.today() + timedelta(days=90)
    }
    return render(request, 'village_banking/requestloan.html', context)
