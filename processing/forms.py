from django import forms
from django.contrib.auth import get_user_model
from .models import *
# from sales.models import Sale, Invoice, CreditSale, CreditInvoice
# from customers.models import Customer
from shop.models import Inventory
from django.http import HttpResponse, JsonResponse, Http404

User = get_user_model()


class InventoryForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "autocomplete": "off",
            }
        )
    )
    # price = forms.IntegerField(
    #     label='Sale Price',
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Sale Price",
    #         }
    #     )
    # )
    # cost_price = forms.IntegerField(
    #     label='Cost Price',
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Cost Price",
    #         }
    #     )
    # )

    class Meta:
        model = Product
        fields = [
            'title',
        ]
        exclude = [
            'added_date'
        ]


class PurchaseForm(forms.ModelForm):
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
    price = forms.IntegerField(
        label='Cost Price',
        widget=forms.TextInput(
            attrs={
                "class": "number form-control",
                "placeholder": "Cost Price",
                "autocomplete": "off",
            }
        )
    )
    quantity = forms.DecimalField(
        label='Quantity (Kg)',
        widget=forms.TextInput(
            attrs={
                "class": "number1 form-control",
                "placeholder": "Quantity (kg)",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = SupplySale
        fields = [
            'item',
            'price',
            'quantity',
        ]
        exclude = [
            'added_date'
        ]


class PurchaseInvoiceForm(forms.ModelForm):
    description = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = SupplyInvoice
        fields = [
            'description',
        ]
        exclude = [
            'added_date'
        ]


class ProcessingForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Inventory.objects.all().order_by('title'),
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

    class Meta:
        model = ProcessingInvoice
        fields = [
            'item',
            'quantity',
        ]
        exclude = [
            'added_date'
        ]


class ProcessSaleForm(forms.ModelForm):
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
    # price = forms.IntegerField(
    #     required=False,
    #     label='Price',
    #     help_text='Hold down "Control" to select more.',
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Price",
    #         }
    #     )
    # )

    class Meta:
        model = ProcessingSale
        fields = [
            'item',
            'quantity',
        ]
        exclude = [
            'added_date'
        ]
