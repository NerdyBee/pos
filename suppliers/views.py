from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SuppliersForm, CreditForm, LoanForm, DebtForm
import datetime
import csv
from django.http import HttpResponse
from .models import Suppliers, SupplyDeposit

# Create your views here.
from django.core.paginator import Paginator
from .filters import *

now = datetime.datetime.today().strftime('%Y-%m-%d')


@login_required
def supplier_view(request):
    form = SuppliersForm(request.POST or None)
    form_head = 'Suppliers Profile'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = SuppliersForm()
    qs = Suppliers.objects.filter().order_by('name')
    my_filter = SuppliersFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "supplier.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def supplier_receivable_view(request):
    form = SuppliersForm(request.POST or None)
    form_head = 'Suppliers Payable'
    qs = Suppliers.objects.filter().order_by('name')
    return render(request, "receivable.html", {"form": form, "form_head": form_head, "object": qs})


@login_required
def supplier_payable_view(request):
    form = SuppliersForm(request.POST or None)
    form_head = 'Suppliers Receivable'
    qs = Suppliers.objects.filter().order_by('name')
    return render(request, "payable.html", {"form": form, "form_head": form_head, "object": qs})


@login_required
def supplier_edit_view(request, pk):
    obj = Suppliers.objects.get(id=pk)
    # obj = get_object_or_404(OutBank, id=pk)
    form = SuppliersForm(instance=obj)
    form_head = 'Out Bank'
    # print(form.errors)
    if request.method == 'POST':
        form = SuppliersForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/suppliers')
    qs = Suppliers.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = ""
    return render(request, "supplier.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def supplier_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Suppliers, id=pk)
    obj.delete()
    return redirect('/customer')


@login_required
def credit_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = CreditForm(request.POST or None)
    form_head = 'Suppliers Payment'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = CreditForm()
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = SupplyDeposit.objects.filter().order_by('-added_date')
        else:
            qs = SupplyDeposit.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date')
    else:
        qs = SupplyDeposit.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date')
    my_filter = DepositFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "credit.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def credit_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyDeposit, id=pk)
    form = CreditForm(instance=obj)
    form_head = 'Suppliers Payment'
    # print(form.errors)
    if request.method == 'POST':
        form = CreditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/supplier_credit')
    qs = SupplyDeposit.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    page_obj = ""
    return render(request, "credit.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def credit_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyDeposit, id=pk)
    obj.delete()
    return redirect('/supplier_credit')


@login_required
def view_supplier_credit(request, inv=None, *args, **kwargs):
    form_head = 'Receipt'
    # st = SupplyDeposit.objects.get(invoice_no=inv).sale_type
    qs0 = SupplyDeposit.objects.filter(id=inv).order_by('-id')
    for rw in qs0:
        cust = rw.supplier_id
        dt = rw.added_date

    qs1 = Suppliers.objects.filter(id=cust)
    qs = SupplyDeposit.objects.filter(supplier=cust, added_date__date=dt).order_by('-id')
    print(dt)
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = SupplyDeposit.objects.filter(id=inv)
    obj2 = obj1[0]

    return render(request, "supplier_receipt.html", {"form_head": form_head, "object": page_obj, "object1": obj2, "object2": qs1})


@login_required
def loan_view(request):
    form = LoanForm(request.POST or None)
    form_head = 'Loan'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = LoanForm()
    qs = SupplyLoan.objects.filter().order_by('-added_date')
    my_filter = LoanFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def loan_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyLoan, id=pk)
    form = LoanForm(instance=obj)
    form_head = 'Loan'
    # print(form.errors)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/loan')
    qs = SupplyLoan.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def loan_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyLoan, id=pk)
    obj.delete()
    return redirect('/loan')


@login_required
def supplier_debt_view(request):
    form = DebtForm(request.POST or None)
    form_head = 'Debt'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = DebtForm()
    qs = SupplyDebt.objects.filter().order_by('-added_date')
    my_filter = DebtFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "supply_debt.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def supplier_debt_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyDebt, id=pk)
    form = DebtForm(instance=obj)
    form_head = 'Debt'
    # print(form.errors)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/supply_debt')
    qs = SupplyDebt.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "supply_debt.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def supplier_debt_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplyDebt, id=pk)
    obj.delete()
    return redirect('/supply_debt')


def export_receivable(request):
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Suppliers Receivable as at ' + str(now)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Suppliers', 'Phone Number', 'Address', 'Amount'])

    # qs = Inventory.objects.filter().order_by('title')

    qs = Suppliers.objects.filter().order_by('name')

    grand_total = 0
    for row_data in qs:
        if row_data.current_bal < 0:
            writer.writerow([row_data.name, row_data.phone, row_data.address, f"{abs(row_data.current_bal):,.2f}"])
            grand_total += row_data.current_bal

    writer.writerow(['', '', 'Total =', f"{abs(grand_total):,.2f}"])

    return response

