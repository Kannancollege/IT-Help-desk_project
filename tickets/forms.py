from django import forms
from .models import Ticket


class BootstrapFormMixin:
    def _style(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class TicketCreateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['category', 'priority', 'description', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue in detail...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class TicketStatusUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'resolution_notes']
        widgets = {
            'resolution_notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class AssignTechnicianForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['technician', 'priority']

    def __init__(self, *args, **kwargs):
        from accounts.models import User
        super().__init__(*args, **kwargs)
        self.fields['technician'].queryset = User.objects.filter(role=User.Role.TECHNICIAN)
        self._style()
