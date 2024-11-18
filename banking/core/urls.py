from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("", views.home_view, name="home"),  # Example home view
    path("logout/", views.sign_out, name="logout"),
    path(
        "create/", views.create_account_view, name="create_account"
    ),  # URL for account creation
    path("account/", views.account_view, name="account"),  # URL for account details
    path("transfer/", views.fund_transfer, name="fund_transfer"),
    path("bill-payment/", views.bill_payment, name="bill_payment"),
    path("fund_transfer/", views.fund_transfer, name="fund_transfer"),
    path("transaction-history/", views.transaction_history, name="transaction_history"),
    path("bill-history/", views.bill_payment_history, name="bill_history"),
]
