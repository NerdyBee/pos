from django import forms
from django.contrib.auth import get_user_model
from .models import Invoice, Sale, CreditInvoice, CreditSale
from shop.models import Inventory
from processing.models import Product
from customers.models import Customer

User = get_user_model()


class InvoiceForm(forms.ModelForm):
    customer = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
            }
        )
    )
    # sale_type = forms.ChoiceField(
    #     label='',
    #     choices=Invoice.SALES_TYPE_CHOICES,
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "class": "checkbox-inline",
    #             "name": "sale_type"
    #         }
    #     )
    # )

    class Meta:
        model = Invoice
        fields = [
            'customer',
            # 'sale_type',
        ]
        exclude = [
            'added_date'
        ]


class RegInvoiceForm(forms.ModelForm):
    customer_d = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('name'),
        label='Customer',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Customer",
            }
        )
    )
    # sale_type = forms.ChoiceField(
    #     label='',
    #     choices=Invoice.SALES_TYPE_CHOICES,
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "class": "checkbox-inline",
    #             "name": "sale_type"
    #         }
    #     )
    # )

    class Meta:
        model = Invoice
        fields = [
            'customer_d',
            # 'sale_type',
        ]
        exclude = [
            'added_date'
        ]


class SaleForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by('title'),
        label='Item',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Item",
            }
        )
    )
    quantity = forms.DecimalField(
        label='Quantity (Kg)',
        widget=forms.TextInput(
            attrs={
                "class": "number form-control",
                "placeholder": "Quantity",
                "autocomplete": "off",
            }
        )
    )
    price = forms.IntegerField(
        # required=False,
        label='Price',
        help_text='Hold down "Control" to select more.',
        widget=forms.TextInput(
            attrs={
                "class": "number1 form-control",
                "placeholder": "Price",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Sale
        fields = [
            'item',
            'quantity',
            'price',
        ]
        exclude = [
            'added_date'
        ]


class CreditInvoiceForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('name'),
        label='Customer',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Customer",
            }
        )
    )

    class Meta:
        model = CreditInvoice
        fields = [
            'customer'
        ]
        exclude = [
            'added_date'
        ]


class CreditSaleForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by('title'),
        label='Item',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Item",
            }
        )
    )
    quantity = forms.DecimalField(
        label='Quantity (Kg)',
        widget=forms.TextInput(
            attrs={
                "class": "number form-control",
                "placeholder": "Quantity",
                "autocomplete": "off",
            }
        )
    )
    price = forms.IntegerField(
        required=False,
        label='Price',
        widget=forms.TextInput(
            attrs={
                "class": "number1 form-control",
                "placeholder": "Price",
            }
        )
    )

    class Meta:
        model = CreditSale
        fields = [
            'item',
            'quantity',
            'price',
        ]
        exclude = [
            'added_date'
        ]
