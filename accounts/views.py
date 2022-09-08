from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# Create your views here.
from .forms import LoginForm, RegisterForm, ChangePasswordForm, UpdateProfile, RegisterUpdateForm
from django.core.paginator import Paginator

User = get_user_model()


class PasswordsChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'password_success.html', {})


@staff_member_required
def register_view(request):
    form = RegisterForm(request.POST or None)
    form_head = 'Register User'
    if form.is_valid():
        username = form.cleaned_data.get("username")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        admin = form.cleaned_data.get("admin")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(
                username, email, password,
                first_name=first_name,
                last_name=last_name, is_staff=admin,
            )
        except:
            user = None

        if user is not None:
            # login(request, user)
            return redirect("/register?msg=success")
        else:
            request.session['register_error'] = 1  # 1 == True

    qs = User.objects.all().order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "register.html", {"form": form, "form_head": form_head, "object": page_obj})


@staff_member_required
def register_edit_view(request, pk):
    # obj = User.objects.get(id=pk)
    obj = get_object_or_404(User, id=pk)

    # form = RegisterForm()
    form_head = 'Edit User'

    if request.method == 'POST':
        form = RegisterUpdateForm(request.POST, instance=obj)
        # print('second')
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            admin = form.cleaned_data.get("is_staff")
            active = form.cleaned_data.get("is_active")
            # print('third')
            try:
                user = User.objects.filter(pk=pk).update(
                    username=username,
                    first_name=first_name,
                    last_name=last_name, is_staff=admin, is_active=active,
                )
            except:
                user = None

            if user is not None:
                # login(request, user)
                return redirect("/register?msg=success")
            else:
                return redirect("/register")
    else:
        form = RegisterUpdateForm(instance=obj)

    qs = User.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "edit_user.html", {"form": form, "form_head": form_head, "object": page_obj})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/home")
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # user is valid and active -> is_active
                # request.user == user
                login(request, user)
                request.session['username'] = username
                return redirect("/home")
            else:
                # attempt = request.session.get("attempt") or 0
                # request.session['attempt'] = attempt + 1
                # return redirect("/invalid-password")
                request.session['invalid_user'] = 1  # 1 == True
        return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    # request.user == Anon User
    return redirect("/")


def home_view(request):
    return render(request, 'home.html', {"context": " "})
