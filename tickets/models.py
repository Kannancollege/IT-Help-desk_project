from django.conf import settings
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    class Category(models.TextChoices):
        HARDWARE = 'HARDWARE', 'Hardware'
        SOFTWARE = 'SOFTWARE', 'Software'
        NETWORK = 'NETWORK', 'Network'
        ACCOUNT = 'ACCOUNT', 'Account Access'
        OTHER = 'OTHER', 'Other'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    ticket_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tickets_raised'
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    description = models.TextField()
    attachment = models.FileField(upload_to='ticket_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='tickets_assigned', blank=True, null=True
    )
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.ticket_id} - {self.get_category_display()} ({self.get_status_display()})"

    def mark_resolved(self, notes=''):
        self.status = self.Status.RESOLVED
        self.resolution_notes = notes
        self.resolved_at = timezone.now()
        self.save()

    def close(self):
        self.status = self.Status.CLOSED
        self.save()
