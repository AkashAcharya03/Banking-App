from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Transaction, BillPayment, Account
from .forms import TransferForm, BillPaymentForm, AccountCreationForm, CustomUserCreationForm

def signup_view(request):

    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # login(request, user)  # Log the user in immediately after registration
            return redirect("signin")  # Redirect to the home page or wherever you want
        else:
            print("Form errors:", form.errors)  # Debugging form errors
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


# Sign In View


def signin_view(request):

    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "signin.html")


# Ensure the user is logged in
@login_required
def account_view(request):
    # Get the user from the session
    user = request.user  # The currently logged-in user

    # Fetch the user's account details. Assumes one account per user.
    try:
        account = Account.objects.get(
            user=user
        )  # Retrieves the account for the logged-in user
    except Account.DoesNotExist:
        account = None  # If the user doesn't have an account, set it to None

    return render(request, "account.html", {"user": user, "account": account})


@login_required
def create_account_view(request):
    # Check if the user already has an account
    if Account.objects.filter(user=request.user).exists():
        # If user already has an account, redirect to their account details page
        return redirect("home")

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)  # Do not save to DB yet
            account.user = request.user  # Link the account to the currently logged-in user

            # Automatically generate the account number
            last_account = Account.objects.order_by("id").last()
            if last_account:
                new_account_number = int(last_account.account_number) + 1
            else:
                new_account_number = 20000001
            account.account_number = str(new_account_number)  # Assign the new account number

            account.save()  # Save the account to the database
            return redirect("home")  # Redirect to the account details page
    else:
        form = AccountCreationForm()

    return render(request, "create_account.html", {"form": form})

@login_required
def fund_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            sender_account_number = form.cleaned_data["sender_account"]
            receiver_account = form.cleaned_data["receiver_account"]
            amount = form.cleaned_data["amount"]

            # Fetch the sender and receiver accounts
            sender_account = Account.objects.get(
                account_number=sender_account_number, user=request.user
            )
            receiver_account = Account.objects.get(
                account_number=receiver_account.account_number
            )

            # Check if the sender has sufficient balance
            if sender_account.balance < amount:
                form.add_error("amount", "Insufficient balance")
            else:
                # Deduct amount from sender's account
                sender_account.balance -= amount
                sender_account.save()

                # Add amount to receiver's account
                receiver_account.balance += amount
                receiver_account.save()

                # Save the transaction details to the database
                transaction = Transaction.objects.create(
                    sender=sender_account, receiver=receiver_account, amount=amount
                )

                # Optionally, you can store a success message or log
                print(f"Transaction successful: {transaction}")

                # Optionally, save the transaction details to the database (if you have a Transaction model)
                # Transaction.objects.create(sender=sender_account, receiver=receiver_account, amount=amount)

                return redirect("home")  # Redirect to transaction history page

    else:
        # Automatically set the sender account as the logged-in user's account
        sender_account = Account.objects.get(user=request.user)
        form = TransferForm(initial={"sender_account": sender_account.account_number})

    return render(request, "transfer.html", {"form": form})


@login_required
def bill_payment(request):
    try:
        # Get the account linked to the logged-in user
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "No account found for the current user.")
        return redirect("account")
    except Account.MultipleObjectsReturned:
        messages.error(
            request, "Multiple accounts found for the user. Please contact support."
        )
        return redirect("account")

    if request.method == "POST":
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_payment = form.save(commit=False)  # Don't save to the DB yet
            bill_payment.account = (
                account  # Set the account to the logged-in user's account
            )

            # Check if the account has sufficient balance
            if account.balance >= bill_payment.amount:
                account.balance -= bill_payment.amount
                account.save()  # Update account balance
                bill_payment.save()  # Save the bill payment
                messages.success(
                    request,
                    f"Bill payment for {bill_payment.bill_name} of ₹{bill_payment.amount} was successful.",
                )
                return redirect("home")
            else:
                messages.error(request, "Insufficient balance for this bill payment.")
    else:
        form = BillPaymentForm()

    return render(request, "bill_payment.html", {"form": form})


@login_required
def transaction_history(request):
    # Get the sender and receiver transactions for the logged-in user
    transactions_as_sender = Transaction.objects.filter(sender__user=request.user)
    transactions_as_receiver = Transaction.objects.filter(receiver__user=request.user)

    # Combine both lists of transactions
    transactions = transactions_as_sender | transactions_as_receiver

    # Optionally, you can order the transactions by timestamp
    transactions = transactions.order_by("-timestamp")

    return render(request, "transaction_history.html", {"transactions": transactions})


@login_required
def home_view(request):

    user = request.user  # The currently logged-in user

    # Fetch the user's account details. Assumes one account per user.
    try:
        account = Account.objects.get(
            user=user
        )  # Retrieves the account for the logged-in user
    except Account.DoesNotExist:
        account = None

    username = request.user.username
    return render(
        request, "home.html", {"username": username, "user": user, "account": account}
    )


@login_required
def sign_out(request):
    logout(request)
    return redirect("signin")


@login_required
def bill_payment_history(request):
    payments = BillPayment.objects.filter(account__user=request.user).order_by(
        "-payment_date"
    )
    return render(request, "bill_payment_history.html", {"payments": payments})
