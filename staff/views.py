from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StaffForm, DisciplineForm, AttendanceForm
import datetime
import csv
from django.http import HttpResponse
from .models import Staff, Discipline

# Create your views here.
from django.core.paginator import Paginator
from .filters import *

now = datetime.datetime.today().strftime('%Y-%m-%d')

@login_required(login_url='/login/')
def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    form_head = 'Staff Biodata'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, 'Staff added successfully.')
        form = StaffForm()
    qs = Staff.objects.filter().order_by('surname')
    my_filter = StaffFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "add_staff.html", {"form": form, "form_head": form_head })


@login_required(login_url='/login/')
def edit_staff(request, pk):
    obj = get_object_or_404(Staff, id=pk)
    form = StaffForm(instance=obj)
    form_head = 'Edit Staff Biodata'
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Staff edited successfully.')
            form = StaffForm()
            return redirect('/active_staff')
    
    return render(request, "add_staff.html", {"form": form, "form_head": form_head })


@login_required(login_url='/login/')
def staff_view(request):
    form = StaffForm(request.POST or None)
    form_head = 'Active Staff List'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = StaffForm()
    qs = Staff.objects.filter(status=True).order_by('surname')
    my_filter = StaffFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "staff.html", {"form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required(login_url='/login/')
def inactive_staff_view(request):
    form = StaffForm(request.POST or None)
    form_head = 'Inactive Staff List'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = StaffForm()
    qs = Staff.objects.filter(status=False).order_by('surname')
    my_filter = StaffFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "staff.html", {"form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required(login_url='/login/')
def staff_dectivate_view(request, pk):
    obj = get_object_or_404(Staff, id=pk)
    obj.status = False
    obj.save()
    messages.success(request, 'Staff dectivated successfully.')
    return redirect('/inactive_staff')


@login_required(login_url='/login/')
def staff_activate_view(request, pk):
    obj = get_object_or_404(Staff, id=pk)
    obj.status = True
    obj.save()
    messages.success(request, 'Staff activated successfully.')
    return redirect('/active_staff')


@login_required(login_url='/login/')
def view_staff(request, pk, month=None):
    form_head = 'Staff Biodata'

    qs1 = Staff.objects.filter(id=pk).order_by('-id')
    qs = Discipline.objects.filter(staff=pk).order_by('-id')

    # qs2 = Attendance.objects.filter(staff=pk).order_by('-id')
    
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, "slip.html", {"form_head": form_head, "object": page_obj, "object2": qs1})

@login_required(login_url='/login/')
def individual_staff(request, pk, month=None):
    import pandas
    from calendar import monthrange
    from datetime import datetime, date

    form_head = 'Staff Biodata'

    qs1 = Staff.objects.filter(id=pk).order_by('-id')

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

    daily_checkin = []
    daily_breakout = []
    daily_breakin = []
    daily_checkout = []

    for line in page_obj:
        qs2 = Attendance.objects.filter(staff=pk, action="CHECKIN", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs3 = Attendance.objects.filter(staff=pk, action="BREAKOUT", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs4 = Attendance.objects.filter(staff=pk, action="BREAKIN", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs5 = Attendance.objects.filter(staff=pk, action="CHECKOUT", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        if not qs2:
            daily_checkin.append(['-', line.strftime('%A, %B, %d, %Y')])
        else:
            for row in qs2:
                prt = row[0]
                sm = [prt, row[1].strftime('%A, %B, %d, %Y')]
                daily_checkin.append(sm)
        if not qs3:
            daily_breakout.append(['-', line.strftime('%A, %B, %d, %Y')])
        else:
            for rows in qs3:
                prt = rows[0]
                bo = [prt, rows[1]]
                daily_breakout.append(bo)
        if not qs4:
            daily_breakin.append(['-', line.strftime('%A, %B, %d, %Y')])
        else:
            for rowb in qs4:
                prt = rowb[0]
                bi = [prt, rowb[1]]
                daily_breakin.append(bi)
        if not qs5:
            daily_checkout.append(['-', line.strftime('%A, %B, %d, %Y')])
        else:
            for rowc in qs5:
                prt = rowc[0]
                co = [prt, rowc[1]]
                daily_checkout.append(co)

    # qs2 = Attendance.objects.filter(staff=pk).order_by('-id')
    

    return render(request, "individual_report.html", {"form_head": form_head, "object2": qs1, "attend1": daily_checkin, "attend2": daily_breakout, "attend3": daily_breakin, "attend4": daily_checkout})


@login_required(login_url='/login/')
def individual_offence(request, pk):

    form_head = 'Staff Offences'

    qs1 = Staff.objects.filter(id=pk).order_by('-id')
    qs = Discipline.objects.filter(staff=pk).order_by('-id')

    # qs2 = Attendance.objects.filter(staff=pk).order_by('-id')
    
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "offences.html", {"form_head": form_head, "object2": qs1, "object": page_obj})


@login_required(login_url='/login/')
def discipline_view(request):
    form = DisciplineForm(request.POST or None)
    form_head = 'Staff Displinary'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, 'Offence submited successfully.')
        form = DisciplineForm()
    qs = Discipline.objects.filter().order_by('-id')
    my_filter = DisciplineFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "discipline.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required(login_url='/login/')
def edit_discipline(request, pk):
    obj = get_object_or_404(Discipline, id=pk)
    form = DisciplineForm(instance=obj)
    form_head = 'Edit Staff Offence'
    if request.method == 'POST':
        form = DisciplineForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('/view_discipline')
    
    return render(request, "discipline.html", {"form": form, "form_head": form_head, "myFilter": "-" })


@login_required(login_url='/login/')
def discipline_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Discipline, id=pk)
    obj.delete()
    return redirect('/view_discipline')


@login_required(login_url='/login/')
def attendance_view(request):
    form = AttendanceForm(request.POST or None)
    form_head = 'Staff Attendance'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = AttendanceForm()
    qs = Attendance.objects.filter().order_by('-id')
    my_filter = AttendanceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "attendance.html", {"form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required(login_url='/login/')
def attendance_sign(request):
    form = AttendanceForm(request.POST or None)
    form_head = 'Staff Attendance'
    if form.is_valid():
        cd = form.cleaned_data
        check_date = cd.get('check_date')
        stff = cd.get('staff')
        check_action = cd.get('action')
        obj = form.save(commit=False)
        obj.user = request.user
        if not Attendance.objects.filter(staff=stff, action=check_action, check_date__date=check_date.date()).exists():
            obj.save()
            messages.success(request, 'Attendance submited successfully.')
            form = AttendanceForm()
        else:
            messages.warning(request, check_action + ' for today is already submitted.')
            form = AttendanceForm()

    qs = Attendance.objects.filter().order_by('-id')
    my_filter = AttendanceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "add_attendance.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})

# @login_required
def home_sign(request):
    form = AttendanceForm(request.POST or None)
    form_head = 'Staff Attendance'
    if form.is_valid():
        cd = form.cleaned_data
        check_date = cd.get('check_date')
        stff = cd.get('staff')
        check_action = cd.get('action')
        obj = form.save(commit=False)
        # obj.user = request.user
        if not Attendance.objects.filter(staff=stff, action=check_action, check_date__date=check_date.date()).exists():
            obj.save()
            messages.success(request, 'Attendance submited successfully.')
            form = AttendanceForm()
        else:
            messages.warning(request, check_action + ' for today is already submitted.')

    qs = Attendance.objects.filter().order_by('-id')
    my_filter = AttendanceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"form": form, "form_head": form_head, "myFilter": " "})


@login_required(login_url='/login/')
def edit_attendance(request, pk):
    obj = get_object_or_404(Attendance, id=pk)
    form = AttendanceForm(instance=obj)
    form_head = 'Edit Staff Offence'
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Attendance edited successfully.')

            return redirect('/sign')
    
    return render(request, "add_attendance.html", {"form": form, "form_head": form_head, "myFilter": "-" })


@login_required(login_url='/login/')
def attendance_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Attendance, id=pk)
    obj.delete()
    messages.success(request, 'Attendance deleted successfully.')
    return redirect('/sign')


@login_required(login_url='/login/')
def daily_attendance(request, timestamp=None):
    form_head = 'Attendance List'
    if timestamp is None:
        now = datetime.date.today().strftime('%Y-%m-%d')
        link = datetime.datetime.strptime(now, '%Y-%m-%d').strftime('%A, %B %d %Y')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
            sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%Y-%m-%d')
            link = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%A, %B %d %Y')
        else:
            sdate = now
            link = sdate
        qs1 = Attendance.objects.filter(check_date__date=sdate).order_by('-added_date')
    else:
        qs1 = Attendance.objects.filter(check_date__date=now).order_by('-added_date')
    
    dt = datetime.date.today().strftime('%A, %B %d %Y')
    qs = Staff.objects.filter(status=True).order_by('surname')
    my_filter = ReportFilter(request.GET, queryset=qs)
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"form_head": form_head, "link": dt, "object": page_obj, "object1": qs1, "myFilter": my_filter})


@login_required(login_url='/login/')
def attendance_days(request, pk, month=None):
    import pandas
    from calendar import monthrange

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    if request.GET.get('month'):
        sch = request.GET.get('month').split("-")
        month = int(sch[1])
        year = int(sch[0])

    num_days = monthrange(year, month)[1]

    sdate = datetime.date(year, month, 1)  # start date
    edate = datetime.date(year, month, num_days)  # end date

    page_obj = pandas.date_range(sdate, edate).tolist()

    daily_checkin = []
    daily_breakout = []
    daily_breakin = []
    daily_checkout = []

    for line in page_obj:
        qs = Attendance.objects.filter(staff=pk, action="CHECKIN", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs1 = Attendance.objects.filter(staff=pk, action="BREAKOUT", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs2 = Attendance.objects.filter(staff=pk, action="BREAKIN", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        qs3 = Attendance.objects.filter(staff=pk, action="CHECKOUT", check_date__date=line.strftime('%Y-%m-%d')).values('check_date__time').values_list('check_date__time', 'check_date__date')
        if not qs:
            daily_checkin.append(['-', line.strftime('%b, %d, %Y')])
        else:
            for row in qs:
                prt = row[0]
                sm = [prt, row[1]]
                daily_checkin.append(sm)
        if not qs1:
            daily_breakout.append(['-', line.strftime('%b, %d, %Y')])
        else:
            for rows in qs1:
                prt = rows[0]
                bo = [prt, rows[1]]
                daily_breakout.append(bo)
        if not qs2:
            daily_breakin.append(['-', line.strftime('%b, %d, %Y')])
        else:
            for rowb in qs2:
                prt = rowb[0]
                bi = [prt, rowb[1]]
                daily_breakin.append(bi)
        if not qs3:
            daily_checkout.append(['-', line.strftime('%b, %d, %Y')])
        else:
            for rowc in qs3:
                prt = rowc[0]
                co = [prt, rowc[1]]
                daily_checkout.append(co)

    return render(request, "monthly_attendance.html", {"object": daily_checkin, "object1": daily_breakout, "object2": daily_breakin, "object3": daily_checkout})

