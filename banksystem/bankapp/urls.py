from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_page, name='register'),
    path('', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/', home, name='home'),
    path('account/', account, name='account'),
    path('openaccount/', open_bank_account, name='openaccount'),
    path('deposit/', deposit, name='deposit'),
    path('credit/', credit, name='credit'),
    path('installment/', installment, name='installment'),
    path('cashin/', cash_in, name='cash_in'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
]

