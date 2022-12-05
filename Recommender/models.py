from django.db import models
from django.contrib.auth.models import User
# Create your models here.


from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify




class Course(models.Model):
    title = models.CharField(max_length=70)
    schools = models.CharField(max_length=70)
    tution_fees = models.CharField(max_length=70)
    image = models.ImageField(upload_to="Course_image")
    academic_year = models.CharField(max_length=70)
    entry_year=models.CharField(max_length=4, blank=True, null= True)

    description = models.TextField(
        max_length=5000, blank=True, null=True,
        default='Description should contain course details')

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    lectures = models.CharField(max_length=30, blank=True, null=True)
    school_phone = models.CharField(max_length=13,  blank=True, null=True)
    intake_in = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)

    school_email = models.CharField(
        max_length=255,  blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return str(self.pk)


@receiver(post_delete, sender=Course)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.author.username + "-" + instance.title + "-" + instance.schools + "-" + instance.location + "-" + instance.faculty)


pre_save.connect(pre_save_post_receiver, sender=Course)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    rating = models.CharField(max_length=70)
    rated_date = models.DateTimeField(auto_now_add=True)


class Deleted_Course(models.Model):
    user = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    course_id = models.CharField(max_length=255, default='none')
    date = models.DateTimeField(auto_now_add=True)


class Updated_Course(models.Model):
    user = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    course_id = models.CharField(max_length=255, default='none')

    date = models.DateTimeField(auto_now_add=True)
