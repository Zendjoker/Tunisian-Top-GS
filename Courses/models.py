# Courses/models.py

from django.db import models
from django.db.models import Sum
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from Users.models import CustomUser, Professor

# Create your models here.
class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Trading', 'Trading'),
        ('Development', 'Development'),
        ('Design', 'Design UI / UX'),
        ('Data Science', 'Data Science'),
        ('Marketing', 'Marketing'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0, blank=True, null=True)
    img = models.ImageField(upload_to="Course_img", blank=True, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    members_count = models.IntegerField(default=0)
    course_requirements = models.TextField(blank=True, null=True)
    course_features = models.TextField(blank=True, null=True)
    video_trailer = models.FileField(upload_to="course_trailers", blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def course_image(self):
        if self.img and hasattr(self.img, 'url'):
            return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.img.url))
        else:
            return "No Image"

    def calculate_progress_percentage(self, user):
        total_levels = self.admin_levels.count()
        if total_levels == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self)
        completed_levels = user_progress.completed_levels.count()
        return (completed_levels / total_levels) * 100

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self)
        all_levels_completed = all(level in user_progress.completed_levels.all() for level in self.admin_levels.all())
        if all_levels_completed:
            user_progress.completed = True
            user_progress.save()

    def get_total_price(self):
        return self.price - self.discount_price

    def get_next_payment(self):
        return self.discount_price

    def __str__(self):
        return self.title


class Level(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_levels', blank=True, null=True)
    image = models.ImageField(upload_to="levels_images", blank=True, null=True)
    level_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title    

    def videos_count(self):
        modules = self.modules.all()
        total_videos = 0
        for module in modules:
            total_videos += module.videos.count()
        return total_videos

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        if all(module in user_progress.completed_modules.all() for module in self.modules.all()):
            user_progress.completed_levels.add(self)
            self.course.update_completion_status(user)

    def calculate_progress_percentage(self, user):
        total_modules = self.modules.count()
        if total_modules == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        completed_modules = user_progress.completed_modules.filter(level=self).count()
        return (completed_modules / total_modules) * 100


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_modules')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    index = models.IntegerField(default=0)
    module_number = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    open_videos = models.BooleanField(default=False)


    def update_completion_status(self, user=None):
        if user:
            user_progress = UserCourseProgress.objects.get(user=user, course=self.level.course)
            if all(video in user_progress.completed_videos.all() for video in self.videos.all()):
                user_progress.completed_modules.add(self)
                self.level.update_completion_status(user)

    def calculate_progress_percentage(self, user):
        total_videos = self.videos.count()
        if total_videos == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self.level.course)
        completed_videos = user_progress.completed_videos.filter(module=self).count()
        return (completed_videos / total_videos) * 100

    def get_next_module(self):
        next_module = Module.objects.filter(level=self.level, index__gt=self.index).exclude(id=self.id). order_by('index').first()
        return next_module

    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_videos')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="coursesVideos", max_length=100, blank=True, null=True)
    summary = CKEditor5Field(config_name='extends', blank=True, null=True)
    notes = CKEditor5Field(config_name='extends', blank=True, null=True)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.module:
            self.module.update_completion_status()

    def get_next_video(self):
        next_video = Video.objects.filter(module=self.module, index__gt=self.index).order_by('index').first()
        return next_video if next_video else None

    def is_unlocked(self, customuser):
        if self.module.open_videos:
            return True
        if self.index == 0:
            return True
        previous_video = Video.objects.filter(module=self.module, index__lt=self.index).order_by('-index').first()
        if not previous_video:
            return True
        user_progress = UserCourseProgress.objects.get(user=customuser, course=self.course)
        return previous_video in user_progress.completed_videos.all()

    def __str__(self):
        return self.title


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_quizzes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    answer = models.ForeignKey("Courses.QuizOption", on_delete=models.CASCADE,blank=True, null=True ,related_name='quiz_answer')

class QuizOption(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='options')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="quiz_images", blank=True, null=True)

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', blank=True, null=True)
    name = models.CharField(max_length=255)
    quizzes = models.ManyToManyField(Quiz)


class UserCourseProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_levels = models.ManyToManyField(Level, blank=True, related_name='completed_levels')
    completed_modules = models.ManyToManyField(Module, blank=True, related_name='completed_modules')
    completed_videos = models.ManyToManyField(Video, blank=True, related_name='completed_videos')

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        if all(level in user_progress.completed_levels.all() for level in self.course.admin_levels.all()):
            user_progress.completed = True
            user_progress.save()


class LevelProgression(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, related_name='level_progressions')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, related_name='progressions')
    progress = models.IntegerField(default=0, null=True, blank=True)


class CourseProgression(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, related_name='course_progressions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, related_name='user_progressions')

    def calculate_progression(self):
        course_levels = self.course.admin_levels.all()
        level_progressions = LevelProgression.objects.filter(level__in=course_levels, user=self.user)
        total_progress = level_progressions.aggregate(Sum('progress'))['progress__sum']
        total_progress = total_progress or 0
        return total_progress
