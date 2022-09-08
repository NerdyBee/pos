from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SaleForm, InvoiceForm, CreditInvoiceForm, CreditSaleForm, RegInvoiceForm
from .models import Sale, Invoice, CreditInvoice, CreditSale
from shop.models import Inventory, Expenses
from customers.models import Customer, Deposit, Loan
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q
from _datetime import date
import csv
from django.http import HttpResponse
from .filters import *

# Create your views here.
# now = datetime.datetime.now().strftime("%Y-%m-%d")
# now = date.today().strftime('%Y-%m-%d')


@login_required
def invoice_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = InvoiceForm(request.POST or None)
    form1 = RegInvoiceForm(request.POST or None)
    form_head = 'Sales Invoice'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        count = Invoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.user = request.user
        obj.save()
        form = InvoiceForm()
        lst = Invoice.objects.latest('invoice_no')
        request.session['invoice'] = lst.invoice_no
        # request.session['sale_type'] = lst.sale_type
        return redirect('/invoice')
    elif form1.is_valid():
        cd = form1.cleaned_data
        obj = form1.save(commit=False)
        count = Invoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.customer = form1.instance.customer_d.name
        obj.user = request.user
        obj.save()
        form = InvoiceForm()
        lst = Invoice.objects.latest('invoice_no')
        request.session['invoice'] = lst.invoice_no
        # request.session['sale_type'] = lst.sale_type
        return redirect('/invoice')

    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = Invoice.objects.filter().order_by('-timestamp')
        else:
            qs = Invoice.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-timestamp')
    else:
        qs = Invoice.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-timestamp')
        # qs = Invoice.objects.filter(timestamp__date=date.today().strftime('%Y-%m-%d')).order_by('-timestamp')
    # qs = Invoice.objects.filter(timestamp='2021-11-06').order_by('-timestamp')
    # qs = Invoice.objects.filter(timestamp__date=now).order_by('-timestamp')
    my_filter = InvoiceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # page_obj = qs
    return render(request, "sales.html", {"form": form, "form1": form1, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def sales_view(request):
    form = SaleForm(request.POST or None)
    form_head = 'Sales Invoice'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = request.session.get('invoice')
        # obj.sale_type = request.session.get('sale_type')
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        # obj.cost = form.instance.item.cost_price
        obj.user = request.user
        obj.save()
        form = SaleForm()
        return redirect('/invoice')
    qs = Sale.objects.filter(invoice_no=request.session.get('invoice')).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session['invoice'], '06')
    obj1 = Invoice.objects.filter(id=inv)
    # total_price = Sale.objects.all().annotate(total=Sum('price'))
    # total_price1 = Sale.objects.filter(invoice_no=request.session.get('invoice')).aggregate(Sum('total_cost'))
    obj2 = obj1[0]
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def view_sales(request, inv=None, *args, **kwargs):
    form = SaleForm(request.POST or None)
    form_head = 'Sales Invoice'
    # st = Invoice.objects.get(invoice_no=inv).sale_type
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = inv
        # obj.sale_type = st
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        obj.user = request.user
        obj.save()
        form = SaleForm()
        request.session['invoice'] = inv
        # request.session['sale_type'] = st
        return redirect('/invoice')
    qs = Sale.objects.filter(invoice_no=inv).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = Invoice.objects.filter(id=inv)
    total_price = Sale.objects.all().annotate(total=Sum('price'))
    obj2 = obj1[0]
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def sales_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Sale, id=pk)
    form = SaleForm(instance=obj)
    form_head = 'Sales Invoice'
    # print(form.errors)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # if not form.data['price']:
            #     obj.price = form.instance.item.price
            # else:
            #     obj.price = form.data['price']
            obj.save()
            qs1 = Sale.objects.get(id=pk)
            # invc = request.session.get('invoice')
            request.session['invoice'] = qs1.invoice_no
            return redirect('/invoice')
    qs = Sale.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    qs = Sale.objects.get(id=pk)
    inv = format(qs.invoice_no, '06')
    obj1 = Invoice.objects.filter(id=inv)
    obj2 = obj1[0]
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": '', "object1": obj2})


@login_required
def sales_delete_view(request, pk):
    qs1 = Sale.objects.get(id=pk)
    request.session['invoice'] = qs1.invoice_no
    obj = get_object_or_404(Sale, id=pk)
    obj.delete()
    return redirect('/invoice')


@login_required
def credit_invoice_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = CreditInvoiceForm(request.POST or None)
    form_head = 'Sales Invoice'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        lst = CreditInvoice.objects.latest('id')
        request.session['invoice'] = lst.id
        request.session['customer'] = lst.customer_id
        return redirect('/credit_invoice')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = CreditInvoice.objects.filter().order_by('-timestamp')
        else:
            qs = CreditInvoice.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-timestamp')
    else:
        qs = CreditInvoice.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-timestamp')
        # qs = CreditInvoice.objects.filter(timestamp__date=date.today().strftime('%Y-%m-%d')).order_by('-timestamp')

    # qs = CreditInvoice.objects.filter().order_by('-id')
    my_filter = CreditInvoiceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "credit_sales.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def credit_sale_view(request):
    form = CreditSaleForm(request.POST or None)
    form_head = 'Sales Invoice'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.customer = Customer.objects.get(id=request.session.get('customer'))
        obj.invoice_no = CreditInvoice.objects.last()  # request.session.get('invoice')
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        # obj.cost = form.instance.item.cost_price
        obj.user = request.user
        obj.save()
        form = CreditSaleForm()
        return redirect('/credit_invoice')
    qs = CreditSale.objects.filter(invoice_no=request.session.get('invoice')).order_by('-id')
    qs1 = Customer.objects.filter(id=request.session.get('customer'))
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session['invoice'], '06')
    obj1 = CreditInvoice.objects.filter(id=inv)
    total_price = CreditSale.objects.all().annotate(total=Sum('price'))
    obj2 = obj1[0]
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2, "object2": qs1})


@login_required
def view_credit(request, inv=None, *args, **kwargs):
    form = CreditSaleForm(request.POST or None)
    form_head = 'Sales Invoice'
    cust = CreditInvoice.objects.get(id=inv)
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.customer = Customer.objects.get(id=cust.customer_id)
        # obj.invoice_no = inv
        obj.invoice_no = CreditInvoice.objects.get(id=inv)
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        obj.user = request.user
        obj.save()
        form = CreditSaleForm()
        request.session['invoice'] = inv
        request.session['customer'] = cust.customer_id
        return redirect('/credit_invoice')
    qs = CreditSale.objects.filter(invoice_no=inv).order_by('-id')
    qs1 = Customer.objects.filter(id=cust.customer_id)
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = CreditInvoice.objects.filter(id=inv)
    total_price = CreditSale.objects.all().annotate(total=Sum('price'))

    obj2 = obj1[0]
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2, "object2": qs1})


@login_required
def credit_sale_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(CreditSale, id=pk)
    form = CreditSaleForm(instance=obj)
    form_head = 'Credit Sales'
    # print(form.errors)
    if request.method == 'POST':
        form = CreditSaleForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # if not form.data['price']:
            #     obj.price = form.instance.item.price
            # else:
            #     obj.price = form.data['price']
            obj.save()
            qs1 = CreditSale.objects.filter(id=pk).values_list('invoice_no')
            request.session['invoice'] = qs1[0][0]
            return redirect('/credit_invoice')
    qs = CreditSale.objects.filter(id=pk)
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    qs1 = CreditSale.objects.get(id=pk)
    inv = format(request.session.get('invoice'), '06')
    obj1 = CreditInvoice.objects.filter(id=inv)
    obj2 = obj1
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": '', "object1": obj2})


@login_required
def credit_sale_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    qs1 = CreditSale.objects.filter(id=pk).values_list('invoice_no')
    request.session['invoice'] = qs1[0][0]
    obj = get_object_or_404(CreditSale, id=pk)
    obj.delete()
    return redirect('/credit_invoice')


@login_required
def sales_report_view(request, now=None):
    import datetime
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
            sdate = datetime.datetime.strptime(sdate, '%d-%m-%Y').strftime('%Y-%m-%d')
            link = {sdate}
        else:
            sdate = now
            link = ''
        qs = Invoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        qs = Invoice.objects.filter(timestamp__date=now).order_by('-timestamp')
        link = ''
    my_filter = ReportFilter(request.GET, queryset=qs)
    # qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # page_obj = qs
    return render(request, "sales_report.html", {"object": page_obj, "myFilter": my_filter, "timestamp": link})


@login_required
def credit_report_view(request, now=None):
    import datetime
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
            sdate = datetime.datetime.strptime(sdate, '%d-%m-%Y').strftime('%Y-%m-%d')
            # sdate = date.today().strftime('%Y-%m-%d')
            link = {sdate}
        else:
            sdate = now
            link = ''
        qs = CreditInvoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        qs = CreditInvoice.objects.filter(timestamp__date=now).order_by('-timestamp')
        link = ''
    my_filter = ReportFilter(request.GET, queryset=qs)
    # qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # page_obj = qs
    return render(request, "credit_report.html", {"object": page_obj, "myFilter": my_filter, "timestamp": link})


def export_csv_sales(request, now=None):
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Sales Report as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Invoice Number', 'Payment Method', 'Amount', 'Date'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = Invoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        qs = Invoice.objects.filter(timestamp__date=now).order_by('-timestamp')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0
    for row_data in qs:
        writer.writerow([row_data.customer, row_data.invoice_no, row_data.sale_type, f"{row_data.sum_total:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M"))])
        grand_total += row_data.sum_total
    writer.writerow(['', '', 'Total =', f"{grand_total:,.2f}", ''])

    return response


def export_csv_credit(request, now=None):
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Credit Report as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Invoice Number', 'Amount', 'Date', '', 'Paid', 'Balance'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = CreditInvoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        sdate = now
        qs = CreditInvoice.objects.filter(timestamp__date=now).order_by('-timestamp')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0
    paid_tt = 0
    bal_tt = 0
    cust = []
    for row_data in qs:
        qs1 = Deposit.objects.filter(added_date__date=sdate, customer=row_data.customer).values('customer').annotate(
            total=Sum('amount')).values_list('total')
        if qs1:
            p_amt = qs1[0][0]
        else:
            p_amt = 0
        cust.append(row_data.customer_id)
        bal = row_data.sum_total - p_amt
        writer.writerow([row_data.customer, row_data.id, f"{row_data.sum_total:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M")), '', f"{p_amt:,.2f}", f"{bal:,.2f}"])
        grand_total += row_data.sum_total
        paid_tt += p_amt
        bal_tt += bal
    writer.writerow(['', 'Total =', f"{grand_total:,.2f}", '', '', f"{paid_tt:,.2f}", f"{bal_tt:,.2f}"])
    writer.writerow([])

    qs2 = Deposit.objects.filter(added_date__date=sdate).values('customer').annotate(
        total=Sum('amount')).values_list('total', 'customer')

    writer.writerow(['Customer Payment'])
    cus_p = 0
    cus_b = 0
    for p_row in qs2:
        qs3 = Customer.objects.filter(id=p_row[1]).exclude(id__in=cust)

        for r in qs3:
            cus_p += p_row[0]
            cus_b += r.current_bal
            writer.writerow(
                [r.name, '', f"{p_row[0]:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M")), '', f"{p_row[0]:,.2f}", f"{r.current_bal:,.2f}"])
    writer.writerow(['', 'Total = ', f"{cus_p:,.2f}", '', '', f"{cus_p:,.2f}", f"{cus_b:,.2f}"])
    tt_rec = cus_p + paid_tt
    writer.writerow([])
    writer.writerow(['', 'Total Received = ', '', '', '', f"{tt_rec:,.2f}", ''])

    return response


def export_csv_detail_sales(request, now=None):
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Sales Report with details as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Invoice Number', 'Payment Method', 'Amount', 'Date', '', 'Item', 'Qty', 'Sale Price', 'Amount'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = Invoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        qs = Invoice.objects.filter(timestamp__date=now).order_by('-timestamp')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0

    for row_data in qs:
        if request.GET.get('timestamp'):
            if request.GET.get('timestamp') != '':
                sdate = request.GET.get('timestamp')
            else:
                sdate = now
            qs = Sale.objects.filter(timestamp__date=sdate, invoice_no=row_data.invoice_no).order_by('-timestamp')
        else:
            qs = Sale.objects.filter(timestamp__date=now, invoice_no=row_data.invoice_no).order_by('-timestamp')
        my_filter1 = ReportFilter(request.GET, queryset=qs)
        qs = my_filter1.qs

        writer.writerow([row_data.customer, row_data.invoice_no, row_data.sale_type, f"{row_data.sum_total:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M"))])
        grand_total += row_data.sum_total

        qty = 0
        tt_amt = 0
        for d_row in qs:
            d_amount = d_row.quantity * d_row.price
            writer.writerow(['', '', '', '', '', '', d_row.item, d_row.quantity, f"{d_row.price:,.2f}", f"{d_amount:,.2f}"])
            qty += d_row.quantity
            tt_amt += d_amount

        writer.writerow(['Total ' + row_data.customer, '', '', '', '', '', '', qty, '', f"{tt_amt:,.2f}"])
    writer.writerow(['Total =', '', '', '', '', '', '', '', '', f"{grand_total:,.2f}"])

    return response


def export_csv_detail_credit(request, now=None):
    if now is None:
        now = date.today().strftime('%Y-%m-%d')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Credit Report with details as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Invoice Number', 'Amount', 'Date', '', 'Item', 'Qty', 'Sale Price', 'Amount', '', 'Paid', 'Balance'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = CreditInvoice.objects.filter(timestamp__date=sdate).order_by('-timestamp')
    else:
        sdate = now
        qs = CreditInvoice.objects.filter(timestamp__date=now).order_by('-timestamp')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0
    paid_tt = 0
    bal_tt = 0
    cust = []
    for row_data in qs:
        if request.GET.get('timestamp'):
            if request.GET.get('timestamp') != '':
                sdate = request.GET.get('timestamp')
            else:
                sdate = now
            qs = CreditSale.objects.filter(timestamp__date=sdate, invoice_no=row_data.id).order_by('-timestamp')
        else:
            qs = CreditSale.objects.filter(timestamp__date=now, invoice_no=row_data.id).order_by('-timestamp')
        my_filter1 = ReportFilter(request.GET, queryset=qs)
        qs = my_filter1.qs

        qs1 = Deposit.objects.filter(added_date__date=sdate, customer=row_data.customer).values('customer').annotate(
            total=Sum('amount')).values_list('total')
        if qs1:
            p_amt = qs1[0][0]
        else:
            p_amt = 0

        cust.append(row_data.customer_id)
        bal = row_data.sum_total - p_amt
        writer.writerow([row_data.customer, row_data.id, f"{row_data.sum_total:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M"))])
        grand_total += row_data.sum_total
        paid_tt += p_amt
        bal_tt += bal
        qty = 0
        tt_amt = 0
        for d_row in qs:
            d_amount = d_row.quantity * d_row.price
            writer.writerow(['', '', '', '', '', d_row.item, d_row.quantity, f"{d_row.price:,.2f}", f"{d_amount:,.2f}"])
            qty += d_row.quantity
            tt_amt += d_amount

        writer.writerow(['Total ' + row_data.customer.name, '', '', '', '', '', qty, '', f"{tt_amt:,.2f}", '', f"{p_amt:,.2f}", f"{bal:,.2f}"])
    writer.writerow(['Grand Total =', '', '', '', '', '', '', '', f"{grand_total:,.2f}", '', f"{paid_tt:,.2f}", f"{bal_tt:,.2f}"])

    writer.writerow([])

    qs2 = Deposit.objects.filter(added_date__date=sdate).values('customer').annotate(
        total=Sum('amount')).values_list('total', 'customer')

    writer.writerow(['Customer Payment'])
    cus_p = 0
    cus_b = 0
    for p_row in qs2:
        qs3 = Customer.objects.filter(id=p_row[1]).exclude(id__in=cust)

        for r in qs3:
            cus_p += p_row[0]
            cus_b += r.current_bal
            writer.writerow(
                [r.name, '', f"{p_row[0]:,.2f}", str(row_data.timestamp.strftime("%d-%m-%Y %H:%M")), '', '', '', '', '',
                 '', f"{p_row[0]:,.2f}", f"{r.current_bal:,.2f}"])
    writer.writerow(['', 'Total = ', f"{cus_p:,.2f}", '', '', '', '', '', '', '', f"{cus_p:,.2f}", f"{cus_b:,.2f}"])
    tt_rec = cus_p + paid_tt
    writer.writerow([])

    tt_tt = tt_rec
    writer.writerow(['Total Received = ', '', '', '', '', '', '', '', '', '', f"{tt_tt:,.2f}", ''])

    return response


@staff_member_required
def profit_report_view(request):
    qs = Inventory.objects.filter().order_by('title')

    return render(request, "profit_report.html", {"object": qs})


@staff_member_required
def purchase_report_view(request):
    from processing.models import Product
    qs = Product.objects.filter().order_by('title')

    return render(request, "sales_summary.html", {"object": qs})


@staff_member_required
def export_csv_profit(request):
    import datetime
    now = datetime.datetime.now()
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Stock Profit as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Sale Price', 'Cost Price', 'Sales', 'Cost Total', 'Sale Total', 'Profit'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = Inventory.objects.filter().order_by('title')
    else:
        sdate = now
        qs = Inventory.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0
    for row_data in qs:
        asset_value = row_data.cost_price * row_data.total_sale_today
        retail_value = row_data.price * row_data.total_sale_today
        prof = retail_value - asset_value

        writer.writerow([row_data.title, f"{row_data.price:,.2f}", f"{row_data.cost_price:,.2f}", row_data.total_sale_today, f"{asset_value:,.2f}", f"{retail_value:,.2f}", f"{prof:,.2f}"])
        grand_total += prof
    writer.writerow(['', '', '', '', '', 'Total', f"{grand_total:,.2f}"])

    return response


@staff_member_required
def export_csv_profit_monthly(request, month=None, year=None):
    import pandas
    from calendar import monthrange
    from datetime import timedelta, datetime

    now = datetime.today().month
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Stock Profit as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'sales', 'cost', 'Profit'])

    if year is None:
        month = datetime.today().month
        year = datetime.today().year

        num_days = monthrange(year, month)[1]

    sdate = date(year, month, 1)  # start date
    edate = date(year, month, num_days)  # end date

    page_obj = pandas.date_range(sdate, edate).tolist()

    for line in page_obj:
        qs = Sale.objects.filter(timestamp__date=line.strftime('%Y-%m-%d')).values('timestamp__date').annotate(
            total=Sum(F('price') * F("quantity")), cost=Sum(F('cost') * F("quantity"))).values_list('total', 'cost')

        for row in qs:
            prt = row[0] - row[1]
            # print(prt)
            writer.writerow([line.strftime('%Y-%m-%d'), row[0], row[1], prt])

    return response


@staff_member_required
def get_days(request, month=None):
    import pandas
    from calendar import monthrange
    from datetime import timedelta, datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    if request.GET.get('month'):
        sch = request.GET.get('month').split("-")
        month = int(sch[1])
        year = int(sch[0])

    num_days = monthrange(year, month)[1]

    sdate = date(year, month, 1)  # start date
    edate = date(year, month, num_days)  # end date

    page_obj = pandas.date_range(sdate, edate).tolist()

    daily = []
    daily_credit = []

    for line in page_obj:
        qs = Sale.objects.filter(timestamp__date=line.strftime('%Y-%m-%d')).values('timestamp__date').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__date')

        qs1 = CreditSale.objects.filter(timestamp__date=line.strftime('%Y-%m-%d')).values('timestamp__date').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__date')

        if not qs:
            daily.append([0, line.strftime('%b, %d, %Y')])
        else:
            for row in qs:
                prt = row[0]
                sm = [prt, row[1]]
                daily.append(sm)

        if not qs1:
            daily_credit.append([0, line.strftime('%b, %d, %Y')])
        else:
            for rows in qs1:
                prt = rows[0]
                sm = [prt, rows[1]]
                daily_credit.append(sm)

    return render(request, "profit_monthly.html", {"object": daily, "object1": daily_credit})


@staff_member_required
def purchase_days(request, month=None):
    import pandas
    from shop.models import PurchaseSale
    from calendar import monthrange
    from datetime import timedelta, datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    if request.GET.get('month'):
        sch = request.GET.get('month').split("-")
        month = int(sch[1])
        year = int(sch[0])

    num_days = monthrange(year, month)[1]

    sdate = date(year, month, 1)  # start date
    edate = date(year, month, num_days)  # end date

    page_obj = pandas.date_range(sdate, edate).tolist()

    daily = []

    for line in page_obj:
        qs = PurchaseSale.objects.filter(timestamp__date=line.strftime('%Y-%m-%d')).values('timestamp__date').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__date')

        if not qs:
            daily.append([0, line.strftime('%b, %d, %Y')])
        else:
            for row in qs:
                prt = row[0]
                sm = [prt, row[1]]
                daily.append(sm)

    return render(request, "purchase_monthly.html", {"object": daily})


@staff_member_required
def get_months(request, year=None):
    import calendar
    from datetime import datetime
    monthly = []
    monthly_credit = []

    if year is None:
        year = datetime.today().year

    if request.GET.get('year'):
        year = request.GET.get('year')

    for i in range(1, 13):
        month = calendar.month_name[i]

        # print(month)

        qs = Sale.objects.filter(timestamp__month=i, timestamp__year=year).values('timestamp__month').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__month')

        qs1 = CreditSale.objects.filter(timestamp__month=i, timestamp__year=year).values('timestamp__month').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__month')

        if not qs:
            monthly.append([0, calendar.month_name[i]])
        else:
            for row in qs:
                prt = row[0]
                mnt = [prt, calendar.month_name[row[1]]]
                monthly.append(mnt)
                # print(mnt)

        if not qs1:
            monthly_credit.append([0, calendar.month_name[i]])
        else:
            for rows in qs1:
                prt = rows[0]
                mnt = [prt, calendar.month_name[rows[1]]]
                monthly_credit.append(mnt)
                # print(mnt)

    return render(request, "profit_yearly.html", {"object": monthly, "object1": monthly_credit, "year": year})


@staff_member_required
def purchase_months(request, year=None):
    import calendar
    from datetime import datetime
    from shop.models import PurchaseSale
    monthly = []

    if year is None:
        year = datetime.today().year

    if request.GET.get('year'):
        year = request.GET.get('year')

    for i in range(1, 13):
        month = calendar.month_name[i]

        qs = PurchaseSale.objects.filter(timestamp__month=i, timestamp__year=year).values('timestamp__month').annotate(
            total=Sum(F('price') * F("quantity"))).values_list(
            'total', 'timestamp__month')

        if not qs:
            monthly.append([0, calendar.month_name[i]])
        else:
            for row in qs:
                prt = row[0]
                mnt = [prt, calendar.month_name[row[1]]]
                monthly.append(mnt)

    return render(request, "purchase_yearly.html", {"object": monthly, "year": year})


def get_forward_month_list(request):
    from datetime import datetime
    from calendar import month_abbr

    month = datetime.now().month   # current month number
    monthly = [month_abbr[(month % 12 + i) or month] for i in range(12)]

    return render(request, "profit_monthly.html", {"object": monthly})

