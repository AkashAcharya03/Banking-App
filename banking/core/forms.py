from django import forms
from .models import Transaction, BillPayment


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Account

from django import forms
from .models import Account

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'balance']  # These are the fields the user will fill out.

    account_number = forms.CharField(max_length=20, required=True)
    balance = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

from django import forms
from .models import Account

class TransferForm(forms.Form):
    sender_account = forms.CharField(max_length=20, required=False)  # Default user account
    receiver_account = forms.ModelChoiceField(queryset=Account.objects.all(), required=True)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    def clean(self):
        cleaned_data = super().clean()
        sender_account = cleaned_data.get('sender_account')
        receiver_account = cleaned_data.get('receiver_account')
        amount = cleaned_data.get('amount')

        # Check if sender and receiver are the same
        if sender_account == receiver_account.account_number:
            raise forms.ValidationError("You cannot transfer money to your own account.")
        
        return cleaned_data


from django import forms
from .models import BillPayment

from django import forms
from .models import BillPayment

class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['bill_name', 'amount']  # Exclude the account field
        widgets = {
            'bill_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
