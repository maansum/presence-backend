# Generated by Django 4.2.1 on 2023-06-29 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_alter_attendees_group_alter_attendees_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmodel',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
