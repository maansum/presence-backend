# Generated by Django 4.2.1 on 2023-06-22 01:35

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofilepic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.get_upload_path),
        ),
        migrations.DeleteModel(
            name='UserProfilePic',
        ),
    ]
