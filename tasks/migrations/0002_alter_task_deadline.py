from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="Task",
            name="deadline",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="Task",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="Task",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="TaskHistory",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="Comment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="Attachment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="Notification",
            name="sent_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]