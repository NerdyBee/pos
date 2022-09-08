import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.contrib.auth import get_user_model

from .models import *
from customers.models import Customer
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
        model = Product
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
        field_name="Name",
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

    class Meta:
        model = SupplyInvoice
        fields = '__all__'
        exclude = ['added_date']


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
    item = CharFilter(
        field_name="item",
        lookup_expr='icontains',
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Item Name",
            }
        )
    )

    quantity = CharFilter(
        field_name="quantity",
        lookup_expr='icontains',
        label="Quantity",
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Quantity",
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

    # sale_type = django_filters.ChoiceFilter(
    #     field_name="sale_type",
    #     choices=SupplyInvoice.SALES_TYPE_CHOICES,
    #     label="Sales Type",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control ms-2",
    #             "placeholder": "Sales Type",
    #         }
    #     )
    # )

    class Meta:
        model = ProcessingInvoice
        fields = '__all__'
        exclude = ['added_date', 'item', 'user']


# class SalesReturnFilter(django_filters.FilterSet):
#     timestamp = DateFilter(
#         label="Added Date",
#         field_name="timestamp",
#         input_formats=['%Y-%m-%d', '%d-%m-%Y'],
#         lookup_expr='contains',
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control ms-2",
#                 "placeholder": "d-m-yyyy",
#             }
#         )
#     )
#     invoice_no = CharFilter(
#         field_name="invoice_no",
#         label="Invoice Number",
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control ms-2",
#                 "placeholder": "Title",
#                 "autocomplete": "off",
#             }
#         )
#     )
#     user = django_filters.ModelChoiceFilter(
#         field_name="User",
#         queryset=User.objects.all(),
#         label="User",
#         widget=forms.Select(
#             attrs={
#                 "class": "form-control ms-2",
#                 "placeholder": "Added By",
#             }
#         )
#     )
#     item = django_filters.ModelChoiceFilter(
#         field_name="item",
#         queryset=Product.objects.all().order_by('title'),
#         label="Item",
#         widget=forms.Select(
#             attrs={
#                 "class": "form-control ms-2",
#                 "placeholder": "Item",
#                 "autocomplete": "off",
#             }
#         )
#     )
#     sale_type = django_filters.ChoiceFilter(
#         field_name="sale_type",
#         choices=SalesReturn.SALES_TYPE_CHOICES,
#         label="Sales Type",
#         widget=forms.Select(
#             attrs={
#                 "class": "form-control ms-2",
#                 "placeholder": "Sales Type",
#             }
#         )
#     )
#
#     class Meta:
#         model = SalesReturn
#         fields = '__all__'
#         exclude = ['added_date', 'quantity', 'price']


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
        model = Product
        fields = '__all__'
        exclude = ['added_date', 'quantity', 'user', 'price', 'title']

