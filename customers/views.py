from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm, DepositForm, LoanForm, DebtForm
import datetime
import csv
from django.http import HttpResponse
from .models import Customer, Deposit

# Create your views here.
from django.core.paginator import Paginator
from .filters import *

now = datetime.datetime.today().strftime('%Y-%m-%d')


@login_required
def customer_view(request):
    form = CustomerForm(request.POST or None)
    form_head = 'Customer Profile'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = CustomerForm()
    qs = Customer.objects.filter().order_by('name')
    my_filter = CustomerFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "customer.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def receivable_view(request):
    form = CustomerForm(request.POST or None)
    form_head = 'Customer Receivable'
    qs = Customer.objects.filter().order_by('name')
    return render(request, "receivable.html", {"form": form, "form_head": form_head, "object": qs})


@login_required
def payable_view(request):
    form = CustomerForm(request.POST or None)
    form_head = 'Customer Payable'
    qs = Customer.objects.filter().order_by('name')
    return render(request, "payable.html", {"form": form, "form_head": form_head, "object": qs})


@login_required
def customer_edit_view(request, pk):
    obj = Customer.objects.get(id=pk)
    # obj = get_object_or_404(OutBank, id=pk)
    form = CustomerForm(instance=obj)
    form_head = 'Out Bank'
    # print(form.errors)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/customer')
    qs = Customer.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "customer.html", {"form": form, "form_head": form_head, "object": ''})


@login_required
def customer_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Customer, id=pk)
    obj.delete()
    return redirect('/customer')


@login_required
def deposit_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year
    form = DepositForm(request.POST or None)
    form_head = 'Customer Deposit'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = DepositForm()
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = Deposit.objects.filter().order_by('-added_date')
        else:
            qs = Deposit.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date')
    else:
        qs = Deposit.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date')
    my_filter = DepositFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "deposit.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def deposit_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Deposit, id=pk)
    form = DepositForm(instance=obj)
    form_head = 'Customer Deposit'
    # print(form.errors)
    if request.method == 'POST':
        form = DepositForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/deposit')
    qs = Deposit.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "deposit.html", {"form": form, "form_head": form_head, "object": ''})


@login_required
def deposit_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Deposit, id=pk)
    obj.delete()
    return redirect('/deposit')


@login_required
def view_deposit(request, inv=None, *args, **kwargs):
    form_head = 'Receipt'
    # st = Deposit.objects.get(invoice_no=inv).sale_type
    qs0 = Deposit.objects.filter(id=inv).order_by('-id')
    for rw in qs0:
        cust = rw.customer_id
        dt = rw.added_date

    qs1 = Customer.objects.filter(id=cust)
    qs = Deposit.objects.filter(customer=cust, added_date__date=dt).order_by('-id')
    print(dt)
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = Deposit.objects.filter(id=inv)
    obj2 = obj1[0]

    return render(request, "receipt.html", {"form_head": form_head, "object": page_obj, "object1": obj2, "object2": qs1})


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
    qs = Loan.objects.filter().order_by('-added_date')
    my_filter = LoanFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def loan_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Loan, id=pk)
    form = LoanForm(instance=obj)
    form_head = 'Loan'
    # print(form.errors)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/loan')
    qs = Loan.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def loan_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Loan, id=pk)
    obj.delete()
    return redirect('/loan')


@login_required
def debt_view(request):
    form = DebtForm(request.POST or None)
    form_head = 'Debt'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = DebtForm()
    qs = Debt.objects.filter().order_by('-added_date')
    my_filter = DebtFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def debt_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Debt, id=pk)
    form = DebtForm(instance=obj)
    form_head = 'Debt'
    # print(form.errors)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/debt')
    qs = Debt.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "loan.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def debt_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Debt, id=pk)
    obj.delete()
    return redirect('/debt')


def export_receivable(request):
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Customer Receivable as at ' + str(now)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Phone Number', 'Address', 'Amount'])

    # qs = Inventory.objects.filter().order_by('title')

    qs = Customer.objects.filter().order_by('name')

    grand_total = 0
    for row_data in qs:
        if row_data.current_bal < 0:
            writer.writerow([row_data.name, row_data.phone, row_data.address, f"{abs(row_data.current_bal):,.2f}"])
            grand_total += row_data.current_bal

    writer.writerow(['', '', 'Total =', f"{abs(grand_total):,.2f}"])

    return response

