import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.contrib.auth import get_user_model

from .models import *
from processing.models import Product
from customers.models import Customer
from suppliers.models import Suppliers
User = get_user_model()


class InventoryFilter(django_filters.FilterSet):
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
    title = CharFilter(
        field_name="title",
        lookup_expr='icontains',
        label="Item Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Name",
            }
        )
    )
    # price = CharFilter(
    #     field_name="price",
    #     lookup_expr='icontains',
    #     label="Sale Price",
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Sale Price",
    #         }
    #     )
    # )
    # cost_price = CharFilter(
    #     field_name="cost_price",
    #     lookup_expr='icontains',
    #     label="Cost Price",
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Cost Price",
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

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['added_date', 'quantity']


class PurchaseFilter(django_filters.FilterSet):
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
    description = CharFilter(
        field_name="description",
        lookup_expr='icontains',
        label="Description",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Name",
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

    sale_type = django_filters.ChoiceFilter(
        field_name="sale_type",
        choices=PurchaseInvoice.SALES_TYPE_CHOICES,
        label="Sales Type",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Sales Type",
            }
        )
    )
    supplier_d = django_filters.ModelChoiceFilter(
        field_name="supplier_d",
        queryset=Suppliers.objects.all().order_by('name'),
        label="Supplier",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Customer",
            }
        )
    )

    class Meta:
        model = PurchaseInvoice
        fields = '__all__'
        exclude = ['added_date']


class ExpensesFilter(django_filters.FilterSet):
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
    title = CharFilter(
        field_name="title",
        label="Title",
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Title",
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
    amount = CharFilter(
        field_name="amount",
        label="Amount",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Amount",
            }
        )
    )

    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ['added_date']


class SupplyFilter(django_filters.FilterSet):
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
    item = django_filters.ModelChoiceFilter(
        field_name="item_id",
        queryset=Inventory.objects.all(),
        label="Item",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Item",
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
    quantity = CharFilter(
        field_name="quantity",
        label="Quantity",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Quantity",
            }
        )
    )

    class Meta:
        model = ProcessSupply
        fields = '__all__'
        exclude = ['added_date']


class ReportFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Date",
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

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['added_date', 'quantity', 'user', 'price', 'title']


class RawReportFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Date",
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

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['added_date', 'user', 'title']

