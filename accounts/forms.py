from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from customers.models import Deposit

# check for unique email & username

User = get_user_model()

non_allowed_usernames = ['abc']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-password",
                "placeholder": "Password",
            }
        )
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-password",
                "placeholder": "Password",
            }
        )
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-confirm-password",
                "placeholder": "Confirm Password",
            }
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Username",
            }
        )
    )
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "First Name",
            }
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Last Name",
            }
        )
    )
    # email = forms.EmailField(
    #     label='Email',
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control form-control-user",
    #             "placeholder": "Email",
    #         }
    #     )
    # )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-password",
                "placeholder": "Password",
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-confirm-password",
                "placeholder": "Confirm Password",
            }
        )
    )
    admin = forms.BooleanField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     qs = User.objects.filter(email__iexact=email)
    #     if qs.exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "Username",
            "label": '',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "id": "user-password",
                "placeholder": "Password",
                "label": '',
            }
        )
    )

    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username


class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    admin = forms.BooleanField(required=False)

    # label = 'Admin',
    # widget = forms.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'admin')

    def save(self, commit=True):
        user = super(self).save(commit=False)

        if commit:
            user.save()

        return user


class RegisterUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Username",
            }
        )
    )
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "First Name",
            }
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Last Name",
            }
        )
    )
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     qs = User.objects.filter(username__iexact=username)
    #     if username in non_allowed_usernames:
    #         raise forms.ValidationError("This is an invalid username, please pick another.")
    #     if qs.exists():
    #         raise forms.ValidationError("This username already exist, please pick another.")
    #     return username

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
        ]

