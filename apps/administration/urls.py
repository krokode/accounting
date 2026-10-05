from django.urls import path
from apps.administration import views

app_name = 'administration'

urlpatterns = [
    path('counterparties/', views.counterparty_list, name='counterparty_list'),
    path('counterparties/create/', views.counterparty_create, name='counterparty_create'),
    path('counterparties/<int:pk>/update/', views.counterparty_update, name='counterparty_update'),
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('company-profile/', views.company_profile_view, name='company_profile'),
]
