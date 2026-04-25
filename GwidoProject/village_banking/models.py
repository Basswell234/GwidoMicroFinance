"""
Village Banking Models
This module defines all the models for the village banking application.
It includes models for managing persons, memberships, investments, transactions,
loans, penalties, interest rates, and loan payments.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    """
    Person model represents an individual in the village banking system.
    It stores personal information and extends the Django User model.
    """
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # Link to Django User for authentication
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    person_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    occupation = models.CharField(max_length=100)
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS_CHOICES)
    membership_desc = models.TextField(blank=True, null=True)
    nrc = models.CharField(max_length=50)  # National Registration Certificate
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        ordering = ['lastname', 'firstname']


# Signal handlers to extend the User profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Person profile when a new User is created"""
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Person profile when User is saved"""
    instance.person.save()


class Membership(models.Model):
    """
    Membership model represents a person's membership in the village banking group.
    It tracks membership details including join date, contribution amount, and role.
    """
    
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('non-member', 'Non-Member'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretary'),
        ('admin', 'Admin'),
    ]
    
    membership_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    join_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.person_id.firstname} - {self.category}"
    
    class Meta:
        ordering = ['-join_date']


class Investment(models.Model):
    """
    Investment model represents an investment or contribution made by a member.
    It tracks the type of investment, amount, and expected return date.
    """
    
    INVESTMENT_CATEGORY_CHOICES = [
        ('monthly contribution', 'Monthly Contribution'),
        ('annual contribution', 'Annual Contribution'),
        ('loan', 'Loan'),
    ]
    
    investment_id = models.AutoField(primary_key=True)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    date = models.DateField()
    investment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=INVESTMENT_CATEGORY_CHOICES)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expected_date = models.DateField()
    
    def __str__(self):
        return f"{self.membership_id.person_id.firstname} - {self.category} ({self.investment_amount})"
    
    class Meta:
        ordering = ['-date']


class Transaction(models.Model):
    """
    Transaction model records all financial transactions (deposits, withdrawals, payments).
    It maintains a detailed history of all monetary movements in the system.
    """
    
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('payment', 'Payment'),
        ('investment', 'Investment'),
        ('penalty', 'Penalty'),
    ]
    
    transaction_id = models.AutoField(primary_key=True)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.membership_id.person_id.firstname} - {self.transaction_type} ({self.amount})"
    
    class Meta:
        ordering = ['-date']


class Loan(models.Model):
    """
    Loan model represents a loan given to a member.
    It tracks loan details including amount, status, collateral, and due date.
    """
    
    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
    ]
    
    loan_id = models.AutoField(primary_key=True)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    collateral_desc = models.TextField(blank=True, null=True)
    loan_issue_date = models.DateField()
    due_date = models.DateField()
    
    def __str__(self):
        return f"{self.membership_id.person_id.firstname} - {self.loan_status} ({self.amount})"
    
    class Meta:
        ordering = ['-loan_issue_date']


class Penalty(models.Model):
    """
    Penalty model represents fines or penalties imposed on members.
    It tracks the penalty amount, status, and the person responsible.
    """
    
    PENALTY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
        ('overdue', 'Overdue'),
    ]
    
    penalty_id = models.AutoField(primary_key=True)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PENALTY_STATUS_CHOICES)
    date = models.DateField()
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.person_id.firstname} - {self.status} ({self.penalty_amount})"
    
    class Meta:
        ordering = ['-date']


class Interest(models.Model):
    """
    Interest model stores the interest rate configuration for the banking system.
    It allows for easy management of interest rates applied to loans and investments.
    """
    
    interest_id = models.AutoField(primary_key=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage value
    interest_desc = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Interest Rate: {self.interest_rate}%"
    
    class Meta:
        ordering = ['-interest_rate']


class Loan_Payment(models.Model):
    """
    Loan_Payment model tracks individual payments made towards loan repayment.
    It records the payment amount, date, and the person making the payment.
    """
    
    loan_payment_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.person_id.firstname} - {self.amount} ({self.date})"
    
    class Meta:
        ordering = ['-date']
