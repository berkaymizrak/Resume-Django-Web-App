# Generated by Django 4.0.6 on 2024-11-29 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_blockeduser_permanent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionlog',
            options={'ordering': ('-created_at', 'id')},
        ),
        migrations.AlterModelOptions(
            name='blockeduser',
            options={'ordering': ('-created_at', 'id')},
        ),
        migrations.AddField(
            model_name='actionlog',
            name='path',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='blockeduser',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='actionlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='actionlog',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='actionlog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='blockeduser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='blockeduser',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='blockeduser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='document',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='generalsetting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='generalsetting',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='generalsetting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='imagesetting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='imagesetting',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='imagesetting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='message',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Silindi'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi'),
        ),
    ]
