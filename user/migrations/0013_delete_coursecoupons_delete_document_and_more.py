# Generated by Django 4.0.6 on 2023-04-23 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_migrate_to_frontend'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseCoupons',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='GeneralSetting',
        ),
        migrations.DeleteModel(
            name='ImageSetting',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='RedirectSlug',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='skill_type',
        ),
        migrations.DeleteModel(
            name='SocialMedia',
        ),
        migrations.DeleteModel(
            name='Statistics',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='SkillTypes',
        ),
    ]