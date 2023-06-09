# Generated by Django 3.2 on 2023-06-09 01:44

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(10000000), django.core.validators.MinValueValidator(99999999)])),
                ('name', models.CharField(max_length=50)),
                ('validity', models.DateField(null=True)),
                ('trail', models.BooleanField(default=False)),
                ('payment_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'license',
                'verbose_name_plural': 'licenses',
                'db_table': 'license',
            },
        ),
    ]
