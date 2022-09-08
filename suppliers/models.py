from django.db import models
from django.conf import settings
from django.db.models import Sum, F

# Create your models here.
User = settings.AUTH_USER_MODEL


class Suppliers(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

    @property
    def total_payment(self):
        current_stock = SupplyDeposit.objects.filter(supplier=self.id).values('supplier').annotate(
            total=Sum('amount')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_credit(self):
        from shop.models import PurchaseSale
        current_stock = PurchaseSale.objects.filter(supplier_d=self.id, sale_type="CR").values('supplier_d').annotate(
            total=Sum(F('price')*F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_debt(self):
        current_stock = SupplyDebt.objects.filter(supplier=self.id).values('supplier').annotate(
            total=Sum('amount')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def current_bal(self):
        cur_bal = self.total_payment - self.total_credit - self.total_debt
        return cur_bal

    def __str__(self):
        return self.name


class SupplyDeposit(models.Model):
    # CASH = 'CS'
    # CREDIT = 'CR'
    # SALES_TYPE_CHOICES = [
    #     ('CS', 'Cash'),
    #     ('CR', 'Credit'),
    # ]
    supplier = models.ForeignKey(Suppliers, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # sale_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)


class SupplyLoan(models.Model):
    supplier = models.ForeignKey(Suppliers, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)


class SupplyDebt(models.Model):
    supplier = models.ForeignKey(Suppliers, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

