from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Transaction, BillPayment, Account


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text="A valid email address is required.",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None  # Optionally remove default Django help texts

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'balance']  # These are the fields the user will fill out.

    account_number = forms.CharField(max_length=20, required=True)
    balance = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

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


class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['bill_name', 'amount']
        widgets = {
            'bill_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Optional: Add custom validation or mark a field as required
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount
