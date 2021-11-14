# Generated by Django 3.1.7 on 2021-10-28 22:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elearn', '0004_auto_20211028_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectsubscribe',
            name='subscriber',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]