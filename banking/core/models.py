from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class Account(models.Model):
    user = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)  # Link each account to a built-in User
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"



class Transaction(models.Model):
    sender = models.ForeignKey(Account, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender.account_number} to {self.receiver.account_number} of {self.amount}"



class BillPayment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Link bill payments to an account
    bill_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_number} paid {self.bill_name}: {self.amount}"
