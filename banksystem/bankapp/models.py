from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    phone = models.CharField(max_length=13, default='', verbose_name='phone')
    passport_number = models.CharField(max_length=20, default='', verbose_name='passport number')
    blocked = models.BooleanField(default=False)
    roles = (
        ('Client', 'Client'),
        ('Operator', 'Operator'),
        ('Administrator', 'Administrator'),
    )
    role = models.CharField(max_length=30, choices=roles, default=roles[0][1])
    banks = models.ManyToManyField('Bank')

    def is_blocked(self):
        return self.blocked

    def __str__(self):
        return self.username

    # @property
    # def balance(self):
    #     if hasattr(self, 'account'):
    #         return self.balance
    #     return 0

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


# class Transaction(models.Model):
#     amount = models.PositiveIntegerField(default=0)
#     date = models.DateField(auto_now_add=date.today())
#     sender = models.ForeignKey('User', on_delete=models.CASCADE)
#     # recipient = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.account.account_no)
#
#     class Meta:
#         ordering = ['timestamp']


class Month(models.Model):
    month_amount = models.PositiveSmallIntegerField(default=0)
    bank = models.ManyToManyField('Bank')

    def __str__(self):
        return str(self.month_amount)


class InterestRate(models.Model):
    interest_rate = models.FloatField(default=1)
    bank = models.ManyToManyField('Bank')

    def __str__(self):
        return str(self.interest_rate)


class Entity(models.Model):
    class Meta:
        abstract = True

    amount = models.PositiveIntegerField(default=0)
    opening_date = models.DateField(auto_now_add=date.today())
    blocked = models.BooleanField(default=False)

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)


class Enterprise(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=100, default='', unique=True)
    email = models.CharField(max_length=50, default='')
    PAN = models.CharField(max_length=9, unique=True, default='')
    address = models.CharField(max_length=150, unique=True, default='')


class Bank(Enterprise):
    BIC = models.CharField(max_length=11, unique=True, default='')

    def __str__(self):
        return self.name


class Company(Enterprise):

    def __str__(self):
        return self.name


class Installment(Entity):
    months = models.ForeignKey('Month', on_delete=models.PROTECT)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return f"Installment of {self.user.username} - {self.amount} $"


class BankAccount(Entity):
    frozen = models.BooleanField(default=False)

    def is_blocked(self):
        return self.block

    def __str__(self):
        return f"{self.user.username} (id: {self.pk})"


class Deposit(Entity):
    months = models.ForeignKey('Month', on_delete=models.PROTECT)
    interest_rate = models.ForeignKey('InterestRate', on_delete=models.PROTECT)


class Credit(Entity):
    months = models.ForeignKey('Month', on_delete=models.PROTECT)
    interest_rate = models.ForeignKey('InterestRate', on_delete=models.PROTECT)
