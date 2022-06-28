from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('api/pnlData/', views.PnlData.as_view()),
    path('balance_sheet/', views.balsheet, name='balsheet'),
    path('balance_sheet/api/balsheetData/', views.BalanceSheetData.as_view()),
    path('cashflow/', views.cashflow, name='cashflow'),
    path('cashflow/api/cashflowData/', views.CashFlowData.as_view())
]
