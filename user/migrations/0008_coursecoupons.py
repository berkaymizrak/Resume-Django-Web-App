# Generated by Django 4.0.6 on 2023-04-01 02:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_redirectslug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCoupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('order', models.IntegerField(default=10, verbose_name='Order')),
                ('course_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Course Name')),
                ('course_url', models.URLField(blank=True, default='', max_length=255, verbose_name='Course URL')),
                ('coupon_code', models.CharField(blank=True, default='', max_length=255, verbose_name='Coupon Code')),
                ('original_price', models.PositiveIntegerField(default=0, verbose_name='Original Price')),
                ('discounted_price', models.PositiveIntegerField(default=0, verbose_name='Discount Price')),
                ('expiration_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Expiration Date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': 'Course Coupon',
                'verbose_name_plural': 'Course Coupons',
                'ordering': ('order',),
            },
        ),
    ]
