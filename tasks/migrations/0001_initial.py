from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("deadline", models.DateTimeField()),
                ("priority", models.CharField(choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")], default="Medium", max_length=10)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed"), ("Cancelled", "Cancelled")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("assigned_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assigned_tasks", to=settings.AUTH_USER_MODEL)),
                ("assigned_to", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to=settings.AUTH_USER_MODEL)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="created_tasks", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TaskHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(max_length=20)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("assigned_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="history_assigned", to=settings.AUTH_USER_MODEL)),
                ("assigned_to", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="history", to="tasks.task")),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="tasks.task")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="attachments/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="tasks.task")),
                ("uploaded_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField()),
                ("type", models.CharField(choices=[("Assignment", "Assignment"), ("Reminder", "Reminder"), ("Overdue", "Overdue")], max_length=20)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tasks.task")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]