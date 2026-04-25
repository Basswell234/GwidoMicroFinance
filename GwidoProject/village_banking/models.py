from django.db import models

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
