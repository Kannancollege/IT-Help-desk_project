from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'employee', 'category', 'priority', 'status', 'technician', 'created_at']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['description', 'employee__username']
