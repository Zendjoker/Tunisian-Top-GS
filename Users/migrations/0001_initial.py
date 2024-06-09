# Generated by Django 5.0.2 on 2024-06-09 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Courses', '0001_initial'),
        ('Products', '0001_initial'),
        ('Ranks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='Badge_img')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('regular', 'Regular'), ('subscriber', 'Subscriber'), ('moderator', 'Moderator')], default='regular', max_length=20)),
                ('tel', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('pfp', models.ImageField(default='default_avatar.png', upload_to='profile_pics/')),
                ('bio', models.TextField(blank=True, max_length=150, null=True)),
                ('last_added_points_time', models.DateTimeField(blank=True, null=True)),
                ('p_general_n', models.BooleanField(default=True)),
                ('p_chat_n', models.BooleanField(default=True)),
                ('p_courses_n', models.BooleanField(default=True)),
                ('email_general_n', models.BooleanField(default=True)),
                ('email_chat_n', models.BooleanField(default=True)),
                ('email_courses_n', models.BooleanField(default=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('points', models.IntegerField(blank=True, default=0, null=True)),
                ('badges', models.ManyToManyField(blank=True, related_name='customusers', to='Users.badge')),
                ('enrolled_courses', models.ManyToManyField(blank=True, related_name='enrolled_users', to='Courses.course')),
                ('liked_products', models.ManyToManyField(blank=True, to='Products.product')),
                ('liked_videos', models.ManyToManyField(blank=True, to='Courses.video')),
                ('rank', models.ManyToManyField(blank=True, to='Ranks.rank')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('line', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='Users.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to='Users.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('profit', 'Profit'), ('loss', 'Loss')], max_length=20, null=True)),
                ('pair', models.CharField(max_length=20, null=True)),
                ('amount', models.FloatField()),
                ('img', models.ImageField(null=True, upload_to='user_transactions')),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='Users.customuser')),
            ],
        ),
    ]
