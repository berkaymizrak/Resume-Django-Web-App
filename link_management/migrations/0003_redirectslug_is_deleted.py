# Generated by Django 4.0.6 on 2024-04-15 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_management', '0002_migrate_from_core'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirectslug',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
