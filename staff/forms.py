from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import *

User = get_user_model()

class StaffForm(forms.ModelForm):
    surname = forms.CharField(
        label='Surname',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Surname",
                "autocomplete": "off",
            }
        )
    )
    firstname = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "autocomplete": "off",
            }
        )
    )
    middlename = forms.CharField(
        label='Middle Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Middle Name",
                "autocomplete": "off",
            }
        )
    )
    contact_address = forms.CharField(
        required=False,
        label='Contact Address',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contact Address",
            }
        )
    )
    residential_address = forms.CharField(
        required=False,
        label='Residential Address',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Residential Address",
            }
        )
    )
    phone = forms.CharField(
        required=False,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone",
                "autocomplete": "off",
            }
        )
    )
    emergency_contact = forms.CharField(
        required=False,
        label='Emergency Contact',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Emergency Contact",
                "autocomplete": "off",
            }
        )
    )
    nationality = forms.CharField(
        required=False,
        label='Nationality',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nationality",
                "autocomplete": "off",
            }
        )
    )
    identification = forms.ChoiceField(
        label='Identification',
        choices=Staff.ID_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "identification"
            }
        )
    )
    employment_status = forms.ChoiceField(
        label='Employee Status',
        choices=Staff.EMPLOYEE_STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Employee Status",
            }
        )
    )
    job_description = forms.ChoiceField(
        required=True,
        label='Job Description',
        choices=Staff.JOB_DESCRIPTION_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Job Description",
            }
        )
    )
    gender = forms.ChoiceField(
        required=True,
        label='Gender',
        choices=Staff.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Gender",
            }
        )
    )
    dob = forms.DateField(
        required=False,
        label='Date of Birth',
        widget=forms.DateInput(
            attrs={
                "class": "form-control mb-3",
                "autocomplete": "off",
                "type": "date",
            },
        )
    )
    genotype = forms.CharField(
        required=False,
        label='Genotype',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Genotype",
                "autocomplete": "off",
            }
        )
    )
    blood_group = forms.CharField(
        required=False,
        label='Blood Group',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Blood Group",
                "autocomplete": "off",
            }
        )
    )
    guardian_name = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Guardian Name",
                "autocomplete": "off",
            }
        )
    )
    guardian_address = forms.CharField(
        required=False,
        label='Contact Address',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contact Address",
                "autocomplete": "off",
            }
        )
    )
    guardian_phone = forms.CharField(
        required=False,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "autocomplete": "off",
            }
        )
    )
    nok_name = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Next of kin Name",
                "autocomplete": "off",
            }
        )
    )
    nok_address = forms.CharField(
        required=False,
        label='Contact Address',
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "NOK Contact Address",
                "autocomplete": "off",
            }
        )
    )
    nok_phone = forms.CharField(
        required=False,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "NOK Phone Number",
                "autocomplete": "off",
            }
        )
    )
    relationship = forms.ChoiceField(
        label='Relationship',
        choices=Staff.NOK_RELATIONSHIP_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "relationship"
            }
        )
    )

    class Meta:
        model = Staff
        fields = [
            'image',
            'surname',
            'firstname',
            'middlename',
            'contact_address',
            'residential_address',
            'phone',
            'emergency_contact',
            'gender',
            'dob',
            'nationality',
            'identification',
            'employment_status',
            'job_description',
            'genotype',
            'blood_group',
            'guardian_name',
            'guardian_address',
            'guardian_phone',
            'nok_name',
            'nok_address',
            'nok_phone',
            'relationship'
        ]
        exclude = [
            'added_date'
        ]

class DisciplineForm(forms.ModelForm):
    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all().order_by('surname'),
        label='Staff',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Staff",
            }
        )
    )
    offence_date = forms.DateField(
        required=False,
        label='Date',
        widget=forms.DateInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Date",
                "autocomplete": "off",
                "type": "date",
            },
        )
    )
    # forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    offence = forms.CharField(
        required=False,
        label='Offence',
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Offence Commited",
                "autocomplete": "off",
            }
        )
    )
    comment = forms.CharField(
        required=False,
        label='Comment',
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Admin Comment",
                "autocomplete": "off",
            }
        )
    )
    action = forms.CharField(
        required=False,
        label='Action',
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Action",
                "autocomplete": "off",
            }
        )
    )
    

    class Meta:
        model = Discipline
        fields = [
            'staff',
            'offence_date',
            'offence',
            'comment',
            'action',
        ]
        exclude = [
            'added_date'
        ]

class AttendanceForm(forms.ModelForm):
    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all().order_by('surname'),
        label='Staff',
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Staff",
            }
        )
    )
    check_date = forms.DateTimeField(
        required=False,
        label='Date',
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Date",
                "autocomplete": "off",
                "type": "datetime-local",
            },
        )
    )
    action = forms.ChoiceField(
        label='Action',
        choices=Attendance.CHECK_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "name": "action"
            }
        )
    )
    

    class Meta:
        model = Attendance
        fields = [
            'staff',
            'check_date',
            'action',
        ]
        exclude = [
            'added_date', 'user'
        ]
    
    # def clean(self):
    #     cleaned_data = self.cleaned_data

    #     try:
    #         Attendance.objects.get(check_date=cleaned_data['check_date'], staff=self.staff)
    #     except Attendance.DoesNotExist:
    #         pass
    #     else:
    #         raise ValidationError('Choose another date')

    #     # Always return cleaned_data
    #     return cleaned_data

