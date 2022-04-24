from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from .constants import *


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'passport_number', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BankAccountForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = ('amount', 'bank')


class CashForm(forms.Form):
    amount = forms.IntegerField(min_value=1)


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = ['amount', 'bank', 'months', 'interest_rate']


class CreditForm(forms.ModelForm):

    class Meta:
        model = Credit
        fields = ['amount', 'bank', 'months', 'interest_rate']


class InstallmentForm(forms.ModelForm):

    class Meta:
        model = Installment
        fields = ['amount', 'company', 'bank', 'months']


class TransactionForm(forms.Form):
    recipient = forms.ModelChoiceField(BankAccount.objects)
    amount = forms.IntegerField(min_value=1)

