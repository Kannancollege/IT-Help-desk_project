from django.urls import path
from . import views

urlpatterns = [
    # Employee
    path('create/', views.create_ticket, name='create_ticket'),
    path('my/', views.my_tickets, name='my_tickets'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    # Technician
    path('assigned/', views.assigned_tickets, name='assigned_tickets'),
    path('<int:ticket_id>/update-status/', views.update_status, name='update_status'),
    path('<int:ticket_id>/close/', views.close_ticket, name='close_ticket'),

    # Admin
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/technicians/', views.manage_technicians, name='manage_technicians'),
    path('admin/all/', views.all_tickets, name='all_tickets'),
    path('admin/<int:ticket_id>/assign/', views.assign_technician, name='assign_technician'),
    path('admin/reports/', views.reports, name='reports'),
]
