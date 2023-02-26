from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager

GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={"required": "Role must be provided"})
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(
        unique=True, blank=False, error_messages={"unique": "A user with that email already exists."}
    )
    mobileno = models.CharField(max_length=10)
    city = models.CharField( max_length=100)
    qualification = models.CharField(max_length=30)
    resume = models.FileField()
    company_description = models.CharField(max_length=500)

    objects = UserManager()

    class Meta:
        ordering = ["id"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    