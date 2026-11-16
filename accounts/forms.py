from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class EmployeeRegisterForm(UserCreationForm):
    """Public registration form - always creates an Employee account.
    Technician/Admin accounts are created by an Admin from the Users panel."""
    email = forms.EmailField(required=True)
    department = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'department', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.EMPLOYEE
        user.email = self.cleaned_data['email']
        user.department = self.cleaned_data.get('department', '')
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class StaffCreateForm(UserCreationForm):
    """Used by Admin to create Technician or Admin accounts."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
