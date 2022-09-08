from django.db import models
from django.conf import settings
from django.db.models import Sum, F

# Create your models here.
User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

    @property
    def total_payment(self):
        current_stock = Deposit.objects.filter(customer=self.id).values('customer').annotate(
            total=Sum('amount')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_credit(self):
        from sales.models import CreditSale
        current_stock = CreditSale.objects.filter(customer=self.id).values('customer').annotate(
            total=Sum(F('price')*F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_loan(self):
        current_stock = Loan.objects.filter(customer=self.id).values('customer').annotate(
            total=Sum('amount')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_debt(self):
        current_stock = Debt.objects.filter(customer=self.id).values('customer').annotate(
            total=Sum('amount')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def current_bal(self):
        cur_bal = self.total_payment - self.total_credit - self.total_loan - self.total_debt
        return cur_bal

    def __str__(self):
        return self.name


class Deposit(models.Model):
    CASH = 'CS'
    CHEQUE = 'CQ'
    SALES_TYPE_CHOICES = [
        ('CS', 'Cash'),
        ('CQ', 'Cheque'),
    ]
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    sale_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)


class Loan(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)


class Debt(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

