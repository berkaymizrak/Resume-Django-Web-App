# Generated by Django 4.0.6 on 2024-04-16 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_actionlog_method'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ('-created_at',), 'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-created_at',), 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterModelOptions(
            name='statistics',
            options={'ordering': ('-created_at',), 'verbose_name': 'Statistic', 'verbose_name_plural': 'Statistics'},
        ),
        migrations.RenameField(
            model_name='actionlog',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='actionlog',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='generalsetting',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='generalsetting',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='imagesetting',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='imagesetting',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='updated_date',
            new_name='updated_at',
        ),
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('ip_address', models.GenericIPAddressField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]