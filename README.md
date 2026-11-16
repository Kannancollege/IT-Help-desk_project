# IT Helpdesk Ticketing System (Django)

A role-based (Employee / Technician / Admin) IT support ticketing system.

## Setup

```bash
pip install -r requirements.txt
python manage.py makemigrations accounts tickets
python manage.py migrate
python manage.py createsuperuser   # create your Admin login
python manage.py runserver
```

Visit http://127.0.0.1:8000/

- Register a normal account → it becomes an **Employee**.
- To create a **Technician** account: log in to `/admin/` with your superuser,
  go to Accounts > Users > Add, and set Role = Technician.
- Superusers you create with `createsuperuser` are NOT automatically given the
  Admin **role** field — after creating one, open `/admin/`, edit that user,
  and set Role = Admin so the app dashboards treat them as Admin.

## Switching from SQLite to MySQL/PostgreSQL

Edit `DATABASES` in `helpdesk/settings.py`, e.g. for MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'helpdesk_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
(install `mysqlclient` via pip first)

## Project structure / roadmap mapping

| Roadmap Step                          | Where it lives |
|----------------------------------------|----------------|
| Step 1-3: HTML/CSS/JS basics           | `templates/base.html`, `static/css/style.css`, Bootstrap CDN |
| Step 4: Django project setup            | `manage.py`, `helpdesk/` |
| Step 5: URLs + Views                    | `accounts/urls.py`, `accounts/views.py`, `tickets/urls.py`, `tickets/views.py` |
| Step 6: Templates                       | `templates/accounts/`, `templates/tickets/` |
| Step 7: Models + DB                     | `accounts/models.py` (User), `tickets/models.py` (Ticket) |
| Step 8: Forms                           | `accounts/forms.py`, `tickets/forms.py` |
| Step 9: CRUD                            | `tickets/views.py` (create/read/update ticket) |
| Step 10: Login/Register                 | `accounts/views.py`, `accounts/urls.py` |
| Step 11: Roles (Employee/Tech/Admin)    | `accounts/models.py` (`Role` choices), `tickets/decorators.py` (`role_required`) |
| Step 12: Ticket assignment              | `tickets/views.py::assign_technician`, `tickets/forms.py::AssignTechnicianForm` |
| Step 13: Status workflow                | `tickets/models.py::Status`, `tickets/views.py::update_status/close_ticket` |
| Step 14: Testing + validation           | Manually verified full flow (register→create→assign→resolve→report) |
| Step 15: Final project + interview prep | This README — use it to walk through architecture in interviews |

## Key models

**User** (`accounts/models.py`): extends Django's `AbstractUser`, adds `role`
(Employee/Technician/Admin), `department`, `phone`.

**Ticket** (`tickets/models.py`): `ticket_id`, `employee` (FK), `category`,
`priority`, `description`, `attachment`, `status`, `technician` (FK, nullable),
`resolution_notes`, `created_at`, `updated_at`, `resolved_at`.

## Access control

`tickets/decorators.py` has a `role_required(*roles)` decorator used on every
view to enforce that only the correct role can access it (e.g. only Employees
can create tickets, only Technicians can update status, only Admins can assign).
