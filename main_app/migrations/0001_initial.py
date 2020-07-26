# Generated by Django 3.0.6 on 2020-06-26 13:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_chat_id', models.IntegerField()),
                ('chat_title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('assigned_users', models.CharField(max_length=128)),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('username', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Choice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('done', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now)),
                ('assigned_users', models.ManyToManyField(to='main_app.User')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminding_type', models.IntegerField(default=2)),
                ('time', models.DateTimeField()),
                ('meeting', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Meeting')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.User')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.User')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Group')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='main_app.User'),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Poll'),
        ),
    ]
