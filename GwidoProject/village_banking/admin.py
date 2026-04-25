from django.contrib import admin
from .models import *

admin.site.register([Person, Membership, Investment, Transaction, Loan, Penalty, Interest, Loan_Payment])

