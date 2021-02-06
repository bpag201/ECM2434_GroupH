from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class Tiers(models.TextChoices):
        STUDENT = "STU", _("Student")
        STAFF = "STF", _("Staff")
        ADMIN = "ADM", _("Admin")
        WELFARE = "WEL", _("Welfare")

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=320)
    nickname = models.CharField(max_length=20)
    course = models.IntegerField()
    score = models.IntegerField()
    resource = models.IntegerField()
    avatar = models.ImageField()
    user_tier = models.CharField(
        max_length=3,
        choices=Tiers.choices,
        default=Tiers.STUDENT
    )
