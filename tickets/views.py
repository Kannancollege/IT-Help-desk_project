from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .decorators import role_required
from .forms import TicketCreateForm, TicketStatusUpdateForm, AssignTechnicianForm
from .models import Ticket


# ---------- Employee ----------

@login_required
@role_required(User.Role.EMPLOYEE)
def create_ticket(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.employee = request.user
            ticket.save()
            messages.success(request, f"Ticket #{ticket.ticket_id} created successfully.")
            return redirect('my_tickets')
    else:
        form = TicketCreateForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})


@login_required
@role_required(User.Role.EMPLOYEE)
def my_tickets(request):
    tickets = Ticket.objects.filter(employee=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    user = request.user
    if user.is_employee() and ticket.employee_id != user.id:
        messages.error(request, "You cannot view this ticket.")
        return redirect('dashboard')
    if user.is_technician() and ticket.technician_id != user.id:
        messages.error(request, "This ticket is not assigned to you.")
        return redirect('dashboard')
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})


# ---------- Technician ----------

@login_required
@role_required(User.Role.TECHNICIAN)
def assigned_tickets(request):
    tickets = Ticket.objects.filter(technician=request.user)
    return render(request, 'tickets/assigned_tickets.html', {'tickets': tickets})


@login_required
@role_required(User.Role.TECHNICIAN)
def update_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id, technician=request.user)
    if request.method == 'POST':
        form = TicketStatusUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.status == Ticket.Status.RESOLVED and not updated.resolved_at:
                from django.utils import timezone
                updated.resolved_at = timezone.now()
            updated.save()
            messages.success(request, f"Ticket #{ticket.ticket_id} updated.")
            return redirect('assigned_tickets')
    else:
        form = TicketStatusUpdateForm(instance=ticket)
    return render(request, 'tickets/update_status.html', {'form': form, 'ticket': ticket})


@login_required
@role_required(User.Role.TECHNICIAN)
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id, technician=request.user)
    ticket.close()
    messages.success(request, f"Ticket #{ticket.ticket_id} closed.")
    return redirect('assigned_tickets')


# ---------- Admin ----------

@login_required
@role_required(User.Role.ADMIN)
def manage_users(request):
    users = User.objects.filter(role=User.Role.EMPLOYEE)
    return render(request, 'tickets/manage_users.html', {'users': users})


@login_required
@role_required(User.Role.ADMIN)
def manage_technicians(request):
    technicians = User.objects.filter(role=User.Role.TECHNICIAN)
    return render(request, 'tickets/manage_technicians.html', {'technicians': technicians})


@login_required
@role_required(User.Role.ADMIN)
def all_tickets(request):
    tickets = Ticket.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    return render(request, 'tickets/all_tickets.html', {
        'tickets': tickets,
        'statuses': Ticket.Status.choices,
        'selected_status': status_filter,
    })


@login_required
@role_required(User.Role.ADMIN)
def assign_technician(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTechnicianForm(request.POST, instance=ticket)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.status = Ticket.Status.IN_PROGRESS
            updated.save()
            messages.success(request, f"Ticket #{ticket.ticket_id} assigned.")
            return redirect('all_tickets')
    else:
        form = AssignTechnicianForm(instance=ticket)
    return render(request, 'tickets/assign_technician.html', {'form': form, 'ticket': ticket})


@login_required
@role_required(User.Role.ADMIN)
def reports(request):
    context = {
        'total': Ticket.objects.count(),
        'open': Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
        'in_progress': Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
        'resolved': Ticket.objects.filter(status=Ticket.Status.RESOLVED).count(),
        'closed': Ticket.objects.filter(status=Ticket.Status.CLOSED).count(),
        'by_category': Ticket.objects.values('category').order_by('category').distinct(),
        'by_priority': Ticket.objects.values('priority').order_by('priority').distinct(),
    }
    return render(request, 'tickets/reports.html', context)
