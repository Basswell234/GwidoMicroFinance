from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
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
    nrc = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        ordering = ['lastname', 'firstname']
    
#extending user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.person.save()


class Membership(models.Model):
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
    interest_id = models.AutoField(primary_key=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_desc = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Interest Rate: {self.interest_rate}%"
    
    class Meta:
        ordering = ['-interest_rate']


class Loan_Payment(models.Model):
    loan_payment_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.person_id.firstname} - {self.amount} ({self.date})"
    
    class Meta:
        ordering = ['-date']
