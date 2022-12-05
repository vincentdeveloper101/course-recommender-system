

import random
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.utils import timezone


class User_Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=13)
    county = models.CharField(max_length=255, blank=True, null=True)
    # age= choises eg 16-18, 19-25, 30-40 40+
    staff = models.BooleanField(default=False)
    # password = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=5000, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='Profile_pictures', blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Code(models.Model):
    user = models.OneToOneField(User_Detail, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        self.code = code_string

        super().save(*args, **kwargs)
