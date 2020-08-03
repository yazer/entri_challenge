# Generated by Django 2.2 on 2020-08-01 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateprofile',
            name='user_uid',
        ),
        migrations.RemoveField(
            model_name='interviewerprofile',
            name='user_uid',
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='interviewerprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='InterviewSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_slots', to='usermanagement.InterviewerProfile')),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviewer_slots', to='usermanagement.InterviewerProfile')),
            ],
        ),
    ]