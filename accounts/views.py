from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import EmployeeRegisterForm, StyledAuthenticationForm
from .models import User
from tickets.models import Ticket


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = EmployeeRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = StyledAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def dashboard(request):
    user = request.user

    if user.is_employee():
        my_tickets = Ticket.objects.filter(employee=user).order_by('-created_at')
        context = {
            'my_tickets': my_tickets,
            'open_count': my_tickets.exclude(status=Ticket.Status.CLOSED).count(),
        }
        return render(request, 'accounts/dashboard_employee.html', context)

    if user.is_technician():
        assigned = Ticket.objects.filter(technician=user).order_by('-created_at')
        context = {
            'assigned_tickets': assigned,
            'open_count': assigned.exclude(status=Ticket.Status.CLOSED).count(),
        }
        return render(request, 'accounts/dashboard_technician.html', context)

    # Admin
    all_tickets = Ticket.objects.all().order_by('-created_at')
    context = {
        'all_tickets': all_tickets,
        'total_tickets': all_tickets.count(),
        'open_tickets': all_tickets.exclude(status=Ticket.Status.CLOSED).count(),
        'total_users': User.objects.filter(role=User.Role.EMPLOYEE).count(),
        'total_technicians': User.objects.filter(role=User.Role.TECHNICIAN).count(),
    }
    return render(request, 'accounts/dashboard_admin.html', context)
