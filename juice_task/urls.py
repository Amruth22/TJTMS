from django.contrib import admin
from django.urls import path
from tasks import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("all-tasks/", views.all_tasks, name="all_tasks"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("task/create/", views.task_create, name="task_create"),
    path("task/<int:task_id>/", views.task_detail, name="task_detail"),
    path("super-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("super-admin/export-csv/", views.export_tasks_csv, name="export_tasks_csv"),
    path("super-admin/delete/<int:task_id>/", views.delete_task, name="delete_task"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)