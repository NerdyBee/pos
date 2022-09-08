from django.db import models
from django.conf import settings
import datetime

# Create your models here.
User = settings.AUTH_USER_MODEL

def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    if instance.pk:
        return 'images/%s_%s.%s' % (instance.surname, instance.pk, extension)
    else:
        return 'images/%s_%s.%s' % (instance.surname, datetime.datetime.now(), extension)

class Staff(models.Model):
    VOTERS_CARD = 'PVC'
    NATIONAL_ID = 'NIN'
    DRIVERS_LICENCE = 'LICENCE'
    PASSPORT = 'PASSPORT'
    ID_TYPE_CHOICES = [
        ('', '----'),
        ('PVC', 'Voters Card'),
        ('NIN', 'National ID'),
        ('LICENCE', 'Drivers Licence'),
        ('PASSPORT', 'Passport'),
    ]
    PARENT = 'PARENT'
    SIBLING = 'SIBLING'
    SPOUSE = 'SPOUSE'
    NOK_RELATIONSHIP_CHOICES = [
        ('', '----'),
        ('PARENT', 'Parent'),
        ('SIBLING', 'Sibling'),
        ('SPOUSE', 'Spouse'),
    ]
    PROBATION ='PROBATION'
    TEMPORARY = 'TEMPORARY'
    PERMANENT = 'PERMANENT'
    EMPLOYEE_STATUS_CHOICES = [
        ('', '----'),
        ('PROBATION', 'Probation'),
        ('TEMPORARY', 'Temporary'),
        ('PERMANENT', 'Permanent'),
    ]
    DRIVER = 'DRIVER'
    SECURITY = 'SECURITY'
    MACHINE_OPERATOR = 'MACHINE OPERATOR'
    NYSC = 'NYSC'
    IT_SIWES = 'IT/SIWES'
    JOB_DESCRIPTION_CHOICES = [
        ('', '----'),
        ('DRIVER', 'Driver'),
        ('SECURITY', 'Security'),
        ('MACHINE OPERATOR', 'Machine Operator'),
        ('NYSC', 'NYSC'),
        ('IT/SIWES', 'IT/SIWES'),
    ]
    FEMALE = 'FEMALE'
    MALE = 'MALE'
    GENDER_CHOICES = [
        ('', '----'),
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
    ]

    surname = models.CharField(max_length=255, null=True, blank=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    middlename = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    identification = models.CharField(max_length=30, choices=ID_TYPE_CHOICES)
    gender = models.CharField(default='MALE', max_length=30, choices=GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=30, choices=EMPLOYEE_STATUS_CHOICES)
    job_description = models.CharField(max_length=50, choices=JOB_DESCRIPTION_CHOICES)
    genotype = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=50, null=True, blank=True)
    contact_address = models.TextField(null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    guardian_name = models.CharField(max_length=255, null=True, blank=True)
    guardian_address = models.TextField(null=True, blank=True)
    guardian_phone = models.CharField(max_length=255, null=True, blank=True)
    nok_name = models.CharField(max_length=255, null=True, blank=True)
    nok_address = models.TextField(null=True, blank=True)
    nok_phone = models.CharField(max_length=255, null=True, blank=True)
    relationship = models.CharField(max_length=30, choices=NOK_RELATIONSHIP_CHOICES)
    status = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to=upload_location, default = 'images/default.png')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True)

    
    def check_in(self, timestamp=None):
        # print(timestamp)
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()
        current_stock = Attendance.objects.filter(staff=self.id, action='CHECKIN', check_date__date=d).values('check_date').values_list('check_date')
        
        if current_stock:
            return current_stock[0][0]
        else:
            return ''
    
    
    def break_out(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()
        current_stock = Attendance.objects.filter(staff=self.id, action='BREAKOUT', check_date__date=d).values('check_date').values_list('check_date')
        if current_stock:
            return current_stock[0][0]
        else:
            return ''
    
    
    def break_in(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()
        current_stock = Attendance.objects.filter(staff=self.id, action='BREAKIN', check_date__date=d).values('check_date').values_list('check_date')
        if current_stock:
            return current_stock[0][0]
        else:
            return ''
    
    
    def check_out(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()
        current_stock = Attendance.objects.filter(staff=self.id, action='CHECKOUT', check_date__date=d).values('check_date').values_list('check_date')
        if current_stock:
            return current_stock[0][0]
        else:
            return ''

    def __str__(self):
        return f'{self.surname} {self.middlename} {self.firstname}'

class Discipline(models.Model):
    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    offence_date = models.DateField()
    offence = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    CHECKIN = "CHECKIN"
    BREAKOUT = "BREAKOUT"
    BREAKIN = "BREAKIN"
    CHECKOUT = "CHECKOUT"
    CHECK_CHOICES = [
        ('', '----'),
        ('CHECKIN', 'Checkin'),
        ('BREAKOUT', 'Breakout'),
        ('BREAKIN', 'Breakin'),
        ('CHECKOUT', 'Checkout'),
    ]

    staff = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    check_date = models.DateTimeField()
    action = models.CharField(max_length=255, choices=CHECK_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
       unique_together = ["staff", "check_date", "action"]

