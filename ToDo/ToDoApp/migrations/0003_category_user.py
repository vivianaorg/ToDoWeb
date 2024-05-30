# Generated by Django 5.0.6 on 2024-05-30 05:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoApp', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(limit_choices_to={'is_superuser': False}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='categorys', to=settings.AUTH_USER_MODEL),
        ),
    ]