# Generated by Django 4.0.6 on 2024-04-15 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_actionlog_is_deleted_document_is_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionlog',
            name='method',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
