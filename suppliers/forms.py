from django import forms
from django.contrib.auth import get_user_model
from .models import Suppliers, SupplyDeposit, SupplyLoan, SupplyDebt

User = get_user_model()


class SuppliersForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "autocomplete": "off",
            }
        )
    )
    phone = forms.CharField(
        required=False,
        label='Phone',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone",
                "autocomplete": "off",
            }
        )
    )
    address = forms.CharField(
        required=False,
        label='Address',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Address",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = Suppliers
        fields = [
            'name',
            'phone',
            'address',
        ]
        exclude = [
            'added_date'
        ]


class CreditForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('name'),
        label='Suppliers',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Suppliers",
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
    # sale_type = forms.ChoiceField(
    #     label='',
    #     choices=SupplyDeposit.SALES_TYPE_CHOICES,
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "class": "checkbox-inline",
    #             "name": "sale_type"
    #         }
    #     )
    # )

    class Meta:
        model = SupplyDeposit
        fields = [
            'supplier',
            'amount',
        ]
        exclude = [
            'added_date'
        ]


class LoanForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('name'),
        label='Suppliers',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Suppliers",
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
    title = forms.CharField(
        required=False,
        label='Description',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = SupplyLoan
        fields = [
            'supplier',
            'amount',
            'title',
        ]
        exclude = [
            'added_date'
        ]


class DebtForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        queryset=Suppliers.objects.all().order_by('name'),
        label='Suppliers',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Suppliers",
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
    title = forms.CharField(
        required=False,
        label='Description',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = SupplyDebt
        fields = [
            'supplier',
            'amount',
            'title',
        ]
        exclude = [
            'added_date'
        ]
