# Generated by Django 3.2 on 2023-06-14 00:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticate', '0001_initial'),
        ('clinical', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Scheduled'), (2, 'Confirmed'), (3, 'Canceled'), (4, 'Finished')], default=1)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('is_return', models.BooleanField(default=False)),
                ('day_off', models.BooleanField(default=False)),
                ('off_reason', models.CharField(blank=True, max_length=150, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.clinic')),
                ('desk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinical.desk')),
                ('pacient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinical.pacient')),
            ],
            options={
                'verbose_name': 'schedule_event',
                'verbose_name_plural': 'schedule_events',
                'db_table': 'schedule_event',
            },
        ),
    ]
