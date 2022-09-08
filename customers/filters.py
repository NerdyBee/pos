import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.contrib.auth import get_user_model

from .models import *
User = get_user_model()


class CustomerFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="added_date",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    name = CharFilter(
        field_name="name",
        lookup_expr='icontains',
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Name",
                "autocomplete": "off",
            }
        )
    )
    phone = CharFilter(
        field_name="phone",
        lookup_expr='icontains',
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Phone Number",
                "autocomplete": "off",
            }
        )
    )
    address = CharFilter(
        field_name="address",
        lookup_expr='icontains',
        label="Address",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Address",
                "autocomplete": "off",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['added_date', 'name']


class DepositFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="added_date",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )
    customer = django_filters.ModelChoiceFilter(
        field_name="customer",
        queryset=Customer.objects.all().order_by('name'),
        label="Customer",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer",
            }
        )
    )
    amount = CharFilter(
        field_name="amount",
        label="Amount",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Amount",
                "autocomplete": "off",
            }
        )
    )
    sale_type = django_filters.ChoiceFilter(
        field_name="sale_type",
        choices=Deposit.SALES_TYPE_CHOICES,
        label="Sales Type",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Sales Type",
            }
        )
    )

    class Meta:
        model = Deposit
        fields = '__all__'
        exclude = ['added_date']


class LoanFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="added_date",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )
    customer = django_filters.ModelChoiceFilter(
        field_name="customer",
        queryset=Customer.objects.all().order_by('name'),
        label="Customer",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer",
            }
        )
    )
    amount = CharFilter(
        field_name="amount",
        label="Amount",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Amount",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['added_date']


class DebtFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="added_date",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )
    customer = django_filters.ModelChoiceFilter(
        field_name="customer",
        queryset=Customer.objects.all().order_by('name'),
        label="Customer",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer",
            }
        )
    )
    amount = CharFilter(
        field_name="amount",
        label="Amount",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Amount",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Debt
        fields = '__all__'
        exclude = ['added_date']
