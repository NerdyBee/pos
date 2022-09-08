import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.contrib.auth import get_user_model

from .models import *
from customers.models import Customer
User = get_user_model()


class InvoiceFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="timestamp",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    invoice_no = CharFilter(
        field_name="invoice_no",
        lookup_expr='icontains',
        label="Invoice Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Invoice Number",
            }
        )
    )
    customer = CharFilter(
        field_name="customer",
        lookup_expr='icontains',
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer Name",
            }
        )
    )
    # user = django_filters.ModelChoiceFilter(
    #     field_name="user",
    #     queryset=User.objects.all(),
    #     label="User",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Added By",
    #         }
    #     )
    # )
    customer_d = django_filters.ModelChoiceFilter(
        field_name="customer_d",
        queryset=Customer.objects.all().order_by('name'),
        label="Reg. Customer",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer",
            }
        )
    )
    # sale_type = django_filters.ChoiceFilter(
    #     field_name="sale_type",
    #     choices=Invoice.SALES_TYPE_CHOICES,
    #     label="Sales Type",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Sales Type",
    #         }
    #     )
    # )

    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ['added_date', 'customer', 'customer_d', 'amount', 'user']


class CreditInvoiceFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Added Date",
        field_name="timestamp",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )
    # invoice_no = CharFilter(
    #     field_name="invoice_no",
    #     label="Invoice Number",
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Invoice Number",
    #         }
    #     )
    # )
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

    class Meta:
        model = CreditInvoice
        fields = '__all__'
        exclude = ['added_date', 'amount']


class ReportFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Date",
        field_name="timestamp",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "d-m-yyyy",
            }
        )
    )


class MonthlyFilter(django_filters.FilterSet):
    month = CharFilter(
        field_name="month",
        label="Month",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Month",
            }
        )
    )
    year = CharFilter(
        field_name="year",
        label="Year",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Year",
            }
        )
    )

    # class Meta:
    #     model = Sale
    #     fields = ['timestamp']