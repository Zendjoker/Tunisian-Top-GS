# Generated by Django 5.0.2 on 2024-06-12 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Courses', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='Users.professor'),
        ),
        migrations.AddField(
            model_name='courseprogression',
            name='course',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_progressions', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='courseprogression',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_progressions', to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='exam',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='level',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_levels', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='levelprogression',
            name='level',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='progressions', to='Courses.level'),
        ),
        migrations.AddField(
            model_name='levelprogression',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='level_progressions', to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_modules', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='module',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='Courses.level'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_quizzes', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='exam',
            name='quizzes',
            field=models.ManyToManyField(to='Courses.quiz'),
        ),
        migrations.AddField(
            model_name='quizoption',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.course'),
        ),
        migrations.AddField(
            model_name='quizoption',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='Courses.quiz'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answer', to='Courses.quizoption'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='completed_levels',
            field=models.ManyToManyField(blank=True, related_name='completed_levels', to='Courses.level'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='completed_modules',
            field=models.ManyToManyField(blank=True, related_name='completed_modules', to='Courses.module'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.course'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercourseprogression', to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='video',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_videos', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='video',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='Courses.module'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='completed_videos',
            field=models.ManyToManyField(blank=True, related_name='completed_videos', to='Courses.video'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='Courses.video'),
        ),
    ]
