from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task, Comment, TaskHistory, Attachment
import csv
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import pytz

@login_required
def dashboard(request):
    # Default time filter: Weekly
    time_filter = request.POST.get("time_filter", "weekly")
    
    # Get IST timezone
    ist = pytz.timezone("Asia/Kolkata")
    today = make_aware(datetime.now(), ist).date()
    
    # Determine date range
    if time_filter == "daily":
        start_date = today
        end_date = today
    elif time_filter == "weekly":
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = start_date + timedelta(days=6)  # Sunday
    else:  # monthly
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    # Convert dates to datetime for filtering
    start_datetime = make_aware(datetime.combine(start_date, datetime.min.time()), ist)
    end_datetime = make_aware(datetime.combine(end_date, datetime.max.time()), ist)
    
    # Debug: Print filter details
    print(f"time_filter: {time_filter}, start: {start_datetime}, end: {end_datetime}")
    
    # Filter tasks assigned to the user
    base_tasks = Task.objects.filter(assigned_to=request.user)
    
    # Split tasks by status with date filter
    pending_tasks = base_tasks.filter(status="Pending", deadline__range=[start_datetime, end_datetime])
    in_progress_tasks = base_tasks.filter(status="In Progress", deadline__range=[start_datetime, end_datetime])
    cancelled_tasks = base_tasks.filter(status="Cancelled", deadline__range=[start_datetime, end_datetime])
    completed_tasks = base_tasks.filter(status="Completed", deadline__range=[start_datetime, end_datetime])
    
    # Debug: Print task counts
    print(f"pending: {pending_tasks.count()}, in_progress: {in_progress_tasks.count()}, cancelled: {cancelled_tasks.count()}, completed: {completed_tasks.count()}")
    
    # Fallback: If no tasks match the filter, show all tasks for the user
    if not (pending_tasks.exists() or in_progress_tasks.exists() or cancelled_tasks.exists() or completed_tasks.exists()):
        pending_tasks = base_tasks.filter(status="Pending")
        in_progress_tasks = base_tasks.filter(status="In Progress")
        cancelled_tasks = base_tasks.filter(status="Cancelled")
        completed_tasks = base_tasks.filter(status="Completed")
        print("Fallback applied: showing all tasks")
    
    return render(request, "dashboard.html", {
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "cancelled_tasks": cancelled_tasks,
        "completed_tasks": completed_tasks,
        "time_filter": time_filter,
    })

@login_required
def all_tasks(request):
    tasks_to = Task.objects.filter(assigned_to=request.user)
    tasks_by = Task.objects.filter(assigned_by=request.user)
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    search = request.GET.get("search")
    if status:
        tasks_to = tasks_to.filter(status=status)
        tasks_by = tasks_by.filter(status=status)
    if priority:
        tasks_to = tasks_to.filter(priority=priority)
        tasks_by = tasks_by.filter(priority=priority)
    if search:
        tasks_to = tasks_to.filter(title__icontains=search)
        tasks_by = tasks_by.filter(title__icontains=search)
    return render(request, "allTasks.html", {
        "tasks_to": tasks_to,
        "tasks_by": tasks_by
    })

@login_required
def task_create(request):
    if request.method == "POST":
        deadline_date = request.POST["deadline_date"]
        deadline_time = request.POST.get("deadline_time") or "23:00"  # Default to 11:00 PM
        # Combine date and time, convert to UTC
        deadline_str = f"{deadline_date} {deadline_time}"
        ist = pytz.timezone("Asia/Kolkata")
        try:
            deadline_local = ist.localize(datetime.strptime(deadline_str, "%Y-%m-%d %H:%M"))
            deadline_utc = deadline_local.astimezone(pytz.UTC)
        except ValueError as e:
            messages.error(request, "Invalid deadline format. Please use a valid date and time.")
            return redirect("task_create")
        task = Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            assigned_to=User.objects.get(id=request.POST["assigned_to"]),
            assigned_by=request.user,
            created_by=request.user,
            deadline=deadline_utc,
            priority=request.POST["priority"],
            status="Pending"
        )
        TaskHistory.objects.create(
            task=task,
            assigned_to=task.assigned_to,
            assigned_by=request.user,
            status=task.status
        )
        messages.success(request, "Task created successfully!")
        return redirect("dashboard")
    users = User.objects.all()
    return render(request, "create.html", {"users": users})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        if "update" in request.POST:
            deadline_date = request.POST["deadline_date"]
            deadline_time = request.POST.get("deadline_time") or "23:00"  # Default to 11:00 PM
            # Combine date and time, convert to UTC
            deadline_str = f"{deadline_date} {deadline_time}"
            ist = pytz.timezone("Asia/Kolkata")
            try:
                deadline_local = ist.localize(datetime.strptime(deadline_str, "%Y-%m-%d %H:%M"))
                deadline_utc = deadline_local.astimezone(pytz.UTC)
            except ValueError as e:
                messages.error(request, "Invalid deadline format. Please use a valid date and time.")
                return redirect("task_detail", task_id=task_id)
            task.status = request.POST["status"]
            task.priority = request.POST["priority"]
            task.assigned_to = User.objects.get(id=request.POST["assigned_to"])
            task.deadline = deadline_utc
            task.description = request.POST["description"]
            task.save()
            TaskHistory.objects.create(
                task=task,
                assigned_to=task.assigned_to,
                assigned_by=request.user,
                status=task.status
            )
            messages.success(request, "Task updated successfully!")
        elif "comment" in request.POST:
            Comment.objects.create(
                task=task,
                user=request.user,
                comment=request.POST["comment"]
            )
            messages.success(request, "Comment added successfully!")
        elif "attachment" in request.POST and request.FILES.get("file"):
            Attachment.objects.create(
                task=task,
                file=request.FILES["file"],
                uploaded_by=request.user
            )
            messages.success(request, "Attachment uploaded successfully!")
    users = User.objects.all()
    return render(request, "detail.html", {
        "task": task,
        "users": users
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    # Get all tasks
    tasks = Task.objects.all()

    # Task counts by priority
    priority_counts = {
        "High": Task.objects.filter(priority="High").count(),
        "Medium": Task.objects.filter(priority="Medium").count(),
        "Low": Task.objects.filter(priority="Low").count(),
    }

    # Task counts by user
    users = User.objects.all()
    user_counts = [(user, Task.objects.filter(assigned_to=user).count()) for user in users]

    # Filter tasks based on GET parameters
    priority_filter = request.GET.get("priority")
    assigned_to_id = request.GET.get("assigned_to")
    user_filter = None

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    elif assigned_to_id:
        user_filter = get_object_or_404(User, id=assigned_to_id)
        tasks = tasks.filter(assigned_to=user_filter)

    return render(request, "admin_dashboard.html", {
        "tasks": tasks,
        "priority_counts": priority_counts.items(),
        "user_counts": user_counts,
        "priority_filter": priority_filter,
        "user_filter": user_filter,
    })

@login_required
def export_tasks_csv(request):
    if not request.user.is_superuser:
        return redirect("dashboard")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(["Title", "Assigned To", "Status", "Priority", "Deadline"])
    tasks = Task.objects.all()
    for task in tasks:
        writer.writerow([task.title, task.assigned_to.username, task.status, task.priority, task.deadline])
    return response

@login_required
def delete_task(request, task_id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        messages.success(request, f"Task '{task.title}' deleted successfully!")
        return redirect("admin_dashboard")
    return redirect("admin_dashboard")