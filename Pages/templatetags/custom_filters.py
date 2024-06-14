from django import template

from Courses.models import UserCourseProgress

register = template.Library()

@register.filter
def is_unlocked(video, user):
    return video.is_unlocked(user)

@register.filter
def is_finished(video, user):
    return video.is_finished(user)

@register.filter
def get_video_icon(video, user):

    return video.get_icon(user)