# Generated by Django 5.0.2 on 2024-03-03 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_customuser_friends_request_customuser_friends"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="access_token",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="customuser",
            name="otp_base32",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="status_2fa",
            field=models.BooleanField(default=False),
        ),
    ]