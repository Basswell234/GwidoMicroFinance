"""
Village Banking Admin Configuration
This module registers all village banking models in the Django admin interface,
allowing administrators to manage persons, memberships, investments, transactions,
loans, penalties, interest rates, and loan payments from the admin dashboard.
"""

from django.contrib import admin
from .models import *

# Register all models in the Django admin
admin.site.register([Person, Membership, Investment, Transaction, Loan, Penalty, Interest, Loan_Payment])

