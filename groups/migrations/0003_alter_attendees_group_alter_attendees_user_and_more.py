# Generated by Django 4.2.1 on 2023-06-27 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0002_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendees',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_id', to='groups.groupmodel'),
        ),
        migrations.AlterField(
            model_name='attendees',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='groupmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='user',
            field=models.ManyToManyField(related_name='groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
