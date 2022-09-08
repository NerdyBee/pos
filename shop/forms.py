from django import forms
from django.contrib.auth import get_user_model
from .models import *
from sales.models import Sale, Invoice, CreditSale, CreditInvoice
from customers.models import Customer
from suppliers.models import Suppliers
from django.http import HttpResponse, JsonResponse, Http404

User = get_user_model()


class ExpensesForm(forms.ModelForm):
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
    amount = forms.IntegerField(
        label='Amount',
        widget=forms.TextInput(
            attrs={
                "class": "number form-control",
                "placeholder": "Amount",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Expenses
        fields = [
            'title',
            'amount',
        ]
        exclude = [
            'added_date'
        ]

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(ExpensesForm, self).clean()

        # extract the username and text field from the data
        title = self.cleaned_data.get('title')
        amount = self.cleaned_data.get('amount')

        # conditions to be met for the username length
        # if len(title) < 5:
        #     # self._errors['title'] = self.error_class([
        #     #     'Minimum 5 characters required'])
        #     raise forms.ValidationError('Minimum 5 characters required')
        # if is_digit(amount) and amount < 1:
        #     self._errors['amount'] = self.error_class([
        #         'Amount Should be a number greater than 1 characters'])

        # return any errors if found
        return self.cleaned_data


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
        model = Inventory
        fields = [
            'title',
        ]
        exclude = [
            'added_date'
        ]


class PurchaseForm(forms.ModelForm):
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
        model = PurchaseSale
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
    # sale_type = forms.ChoiceField(
    #     label='',
    #     choices=PurchaseInvoice.SALES_TYPE_CHOICES,
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "class": "checkbox-inline",
    #             "name": "sale_type"
    #         }
    #     )
    # )

    class Meta:
        model = PurchaseInvoice
        fields = [
            'description',
            # 'sale_type'
        ]
        exclude = [
            'added_date'
        ]


class RegInvoiceForm(forms.ModelForm):
    supplier_d = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('name'),
        label='Supplier',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Supplier",
            }
        )
    )
    sale_type = forms.ChoiceField(
        label='',
        choices=PurchaseInvoice.SALES_TYPE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "checkbox-inline",
                "name": "sale_type"
            }
        )
    )

    class Meta:
        model = PurchaseInvoice
        fields = [
            'supplier_d',
            'sale_type',
        ]
        exclude = [
            'added_date'
        ]


class SupplyForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Inventory.objects.all().order_by('title'),
        label='Product',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Product",
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
        model = ProcessSupply
        fields = [
            'item',
            'quantity',
        ]
        exclude = [
            'added_date'
        ]
