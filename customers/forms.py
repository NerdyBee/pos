from django import forms
from django.contrib.auth import get_user_model
from .models import Customer, Deposit, Loan, Debt

User = get_user_model()


class CustomerForm(forms.ModelForm):
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
            }
        )
    )

    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'address',
        ]
        exclude = [
            'added_date'
        ]


class DepositForm(forms.ModelForm):
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
    sale_type = forms.ChoiceField(
        label='',
        choices=Deposit.SALES_TYPE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "checkbox-inline",
                "name": "sale_type"
            }
        )
    )

    class Meta:
        model = Deposit
        fields = [
            'customer',
            'amount',
            'sale_type',
        ]
        exclude = [
            'added_date'
        ]


class LoanForm(forms.ModelForm):
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
        model = Loan
        fields = [
            'customer',
            'amount',
            'title',
        ]
        exclude = [
            'added_date'
        ]


class DebtForm(forms.ModelForm):
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
        model = Debt
        fields = [
            'customer',
            'amount',
            'title',
        ]
        exclude = [
            'added_date'
        ]
