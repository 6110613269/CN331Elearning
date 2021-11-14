# Generated by Django 3.1.7 on 2021-11-08 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0010_auto_20211105_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='subjectid',
        ),
        migrations.AddField(
            model_name='notification',
            name='subjectid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elearn.subjectsubscribe'),
            preserve_default=False,
        ),
    ]
