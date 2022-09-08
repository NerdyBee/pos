import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.contrib.auth import get_user_model

from .models import *
User = get_user_model()


class StaffFilter(django_filters.FilterSet):
    surname = CharFilter(
        field_name="surname",
        lookup_expr='icontains',
        label="Surname",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Surname",
                "autocomplete": "off",
            }
        )
    )
    firstname = CharFilter(
        field_name="firstname",
        lookup_expr='icontains',
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "autocomplete": "off",
            }
        )
    )
    middlename = CharFilter(
        field_name="middlename",
        lookup_expr='icontains',
        label="Middle Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Middle Name",
                "autocomplete": "off",
            }
        )
    )
    phone = CharFilter(
        field_name="phone",
        lookup_expr='icontains',
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "autocomplete": "off",
            }
        )
    )
    employment_status = django_filters.ChoiceFilter(
        field_name="employment_status",
        choices=Staff.EMPLOYEE_STATUS_CHOICES,
        label="Employee Status",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Employee Status",
            }
        )
    )
    gender = django_filters.ChoiceFilter(
        field_name="gender",
        choices=Staff.GENDER_CHOICES,
        label="Gender",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Gender",
            }
        )
    )
    identification = django_filters.ChoiceFilter(
        field_name="identification",
        choices=Staff.ID_TYPE_CHOICES,
        label="Identification",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "ID Type",
            }
        )
    )
    # user = django_filters.ModelChoiceFilter(
    #     field_name="user",
    #     queryset=User.objects.all(),
    #     label="User",
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Added By",
    #         }
    #     )
    # )

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['added_date', 'image', 'dob', 'user', 'contact_address', 'emergency_contact', 'status', 'nationality', 'residential_address', 'genotype', 'blood_group', 'guardian_name', 'guardian_address', 'guardian_phone', 'nok_name', 'nok_phone', 'nok_address', 'job_description', 'relationship']


class DisciplineFilter(django_filters.FilterSet):
    offence = CharFilter(
        field_name="offence",
        lookup_expr='icontains',
        label="Offence",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Offence",
                "autocomplete": "off",
            }
        )
    )
    offence_date = CharFilter(
        field_name="offence_date",
        lookup_expr='icontains',
        label="Date",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Date",
                "autocomplete": "off",
                "type": "date",
            }
        )
    )
    staff = django_filters.ModelChoiceFilter(
        field_name="staff",
        queryset=Staff.objects.all(),
        label="Staff",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Staff",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )

    class Meta:
        model = Discipline
        fields = '__all__'
        exclude = ['added_date', 'comment', 'action']

class AttendanceFilter(django_filters.FilterSet):
    check_date = CharFilter(
        field_name="check_date",
        lookup_expr='icontains',
        label="Date",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Date",
                "autocomplete": "off",
                "type": "date",
            }
        )
    )
    action = django_filters.ChoiceFilter(
        field_name="action",
        choices=Attendance.CHECK_CHOICES,
        label="Action",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Check Type",
            }
        )
    )
    staff = django_filters.ModelChoiceFilter(
        field_name="staff",
        queryset=Staff.objects.all(),
        label="Staff",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Staff",
            }
        )
    )
    user = django_filters.ModelChoiceFilter(
        field_name="user",
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "Added By",
            }
        )
    )

    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['added_date']

class ReportFilter(django_filters.FilterSet):
    timestamp = DateFilter(
        label="Date",
        field_name="timestamp",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        lookup_expr='contains',
        widget=forms.TextInput(
            attrs={
                "class": "form-control ms-2",
                "placeholder": "dd-mm-yyyy",
                "type": "date",
            }
        )
    )

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['added_date', 'phone', 'dob', 'gender', 'identification', 'employment_status', 'surname', 'firstname', 'middlename', 'image', 'user', 'contact_address', 'emergency_contact', 'status', 'nationality', 'residential_address', 'genotype', 'blood_group', 'guardian_name', 'guardian_address', 'guardian_phone', 'nok_name', 'nok_phone', 'nok_address', 'job_description', 'relationship']