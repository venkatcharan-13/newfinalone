from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('pnl/<str:account>/', views.pnl_transaction, name='transactions'),
    path('api/pnlData/', views.PnlData.as_view()),
    path('balance_sheet/', views.balsheet, name='balsheet'),
    path('balance_sheet/api/balsheetData/', views.BalanceSheetData.as_view()),
    path('cashflow/', views.cashflow, name='cashflow'),
    path('cashflow/<str:activity>/', views.cashflow_balances, name='cfbalances'),
    path('cashflow/api/cashflowData/', views.CashFlowData.as_view()),
    path('ratios/', views.ratios, name='ratios'),
    path('ratios/api/ratiosData/', views.RatiosData.as_view())
]
