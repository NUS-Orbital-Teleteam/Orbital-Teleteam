# Generated by Django 3.0.6 on 2020-07-14 08:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200711_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pushNotifications', models.BooleanField(default=True)),
                ('autoCreateMeetingReminder', models.BooleanField(default=True)),
                ('defaultMeetingReminderTimedelta', models.DurationField(default=datetime.timedelta(seconds=10800))),
                ('autoCreateTaskReminder', models.BooleanField(default=True)),
                ('defaultTaskReminderTimedelta', models.DurationField(default=datetime.timedelta(seconds=36000))),
                ('botDetailedViewOnDefault', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.UserSettings'),
        ),
    ]
