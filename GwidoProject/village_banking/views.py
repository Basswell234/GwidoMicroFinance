"""
Village Banking Views
This module contains views for handling investment, transaction, loan, and other
financial operations in the village banking application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment, Membership, Person
from .forms import InvestmentForm


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
