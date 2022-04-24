from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages

from .models import *
from .forms import *


def home(request):
    context = {
        'title': 'Home',
        'menu_client': menu_client,
        'menu_operator': menu_operator,
        'accounts': BankAccount.objects.all(),
        'user_account': BankAccount.objects.get(user=request.user),
        'deposits': Deposit.objects.filter(user=request.user),
        'credits': Credit.objects.filter(user=request.user),
        'installments': Installment.objects.filter(user=request.user),
    }
    return render(request, 'bankapp/index.html', context=context)


menu_client = [
    {'title': 'Open Account', 'url_name': 'openaccount'},
    {'title': 'Transfer', 'url_name': 'transfer'},
    {'title': 'Deposit', 'url_name': 'deposit'},
    {'title': 'Credit', 'url_name': 'credit'},
    {'title': 'Installment', 'url_name': 'installment'},
    # {'title': 'Cash in', 'url_name': 'cash_in'},
    # {'title': 'Withdraw', 'url_name': 'withdraw'},
]

menu_operator = [
    {'title': 'All Deposits', 'url_name': 'deposit'},
    {'title': 'All Credits', 'url_name': 'credit'},
    {'title': 'All Installments', 'url_name': 'installment'},
]


def register_page(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ' is successfully registered!')
            return redirect('login')

    context = {
        'menu_client': menu_client,
        'title': "Registration",
        'form': form,
    }
    return render(request, 'bankapp/register.html', context=context)


def login_page(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if BankAccount.objects.filter(user=request.user).exists():
                    return redirect('home')
                else:
                    return redirect('openaccount')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect('login')

    context = {
        'menu_client': menu_client,
        'title': 'Authentication',
        'form': form
    }
    return render(request, 'bankapp/login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


def open_bank_account(request):
    if BankAccount.objects.filter(user=request.user).exists():
        return render(request, 'bankapp/account.html', {'menu_client': menu_client, 'title': 'Account', 'accs': BankAccount.objects.all()})
    else:
        form = BankAccountForm

        if request.method == 'POST':
            form = BankAccountForm(request.POST)
            if form.is_valid():
                bank_account = form.save(commit=False)
                bank_account.user = request.user
                bank_account.save()
                return redirect('home')
            # else:
            #     return HttpResponse("Form isn't valid")

        if request.user.is_blocked():
            messages.info(request, 'Operation canceled, you are blocked.')

        context = {
            'menu_client': menu_client,
            'banks': Bank.objects.all(),
            'title': 'Open Account',
            'form': form,
        }

        return render(request, 'bankapp/open_account.html', context=context)


def transfer(request):
    form = TransactionForm()
    sender = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            account = data['recipient']
            amount = data['amount']

            # account = BankAccount.objects.get(pk=account_id)

            if amount > sender.amount:
                messages.info(request, 'No money!')
                return redirect('transfer')
            if account == sender:
                messages.info(request, 'U can\'t transfer to yourself')
                return redirect('transfer')

            sender.amount -= amount
            sender.save()
            account.amount += amount
            account.save()
            return redirect('home')

    context = {
        'menu_client': menu_client,
        'accs': BankAccount.objects.all(),
        'title': 'Transfer',
        'form': form,
    }
    return render(request, 'bankapp/transfer.html', context=context)


def account(request):
    context = {
        'menu_client': menu_client,
        'title': 'Account'
    }
    return render(request, 'bankapp/account.html', context=context)


def deposit(request):
    form = DepositForm()
    sender = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)

        if form.is_valid():
            deposit = form.save(commit=False)
            amount = form.cleaned_data.get('amount')
            deposit.user = request.user
            deposit.save()

            if amount > sender.amount:
                messages.info(request, 'No money!')
                return redirect('deposit')

            sender.amount -= amount
            sender.save()

            return redirect('home')

    if request.user.is_blocked():
        messages.info(request, 'Operation canceled, you are blocked.')

    context = {
        'menu_client': menu_client,
        'menu_operator': menu_operator,
        'title': 'Deposit',
        'form': form,
        'deposits': Deposit.objects.all(),
    }
    return render(request, 'bankapp/deposit.html', context=context)


def credit(request):
    form = CreditForm()
    sender = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreditForm(request.POST)

        if form.is_valid():
            credit = form.save(commit=False)
            amount = form.cleaned_data.get('amount')
            credit.user = request.user
            credit.save()

            sender.amount += amount
            sender.save()

            return redirect('home')

    if request.user.is_blocked():
        messages.info(request, 'Operation canceled, you are blocked.')

    context = {
        'menu_client': menu_client,
        'menu_operator': menu_operator,
        'title': 'Credit',
        'form': form,
        'credits': Credit.objects.all(),
    }
    return render(request, 'bankapp/credit.html', context=context)


def installment(request):
    form = InstallmentForm()

    if request.method == "POST":
        form = InstallmentForm(request.POST)

        if form.is_valid():
            installment = form.save(commit=False)
            installment.user = request.user
            installment.save()

            return redirect('home')

    if request.user.is_blocked():
        messages.info(request, 'Operation canceled, you are blocked.')

    context = {
        'menu_client': menu_client,
        'menu_operator': menu_operator,
        'title': 'Installment',
        'form': form,
        'installments': Installment.objects.all(),
    }
    return render(request, 'bankapp/installment.html', context=context)


def cash_in(request):
    form = CashForm()
    acc = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = CashForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data.get('amount')

            acc.amount += amount
            acc.save()

            return redirect('home')

    context = {
        'menu_client': menu_client,
        'title': 'Cash In',
        'form': form,
    }
    return render(request, 'bankapp/cash.html', context=context)


def withdraw(request):
    form = CashForm()
    acc = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = CashForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data.get('amount')

            if amount > acc.amount:
                messages.info(request, 'No money!')
                return redirect('withdraw')

            acc.amount -= amount
            acc.save()

            return redirect('home')

    context = {
        'menu_client': menu_client,
        'title': 'Withdraw',
        'form': form,
    }
    return render(request, 'bankapp/cash.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found.</h1>')




