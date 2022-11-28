from django.contrib.auth.models import AbstractUser
from django.db import models

SEXE_CHOICES = [
    ('masculin', 'Masculin'),
    ('feminin', 'Féminin'),
]


class CustomUser(AbstractUser):
    birth_date = models.DateTimeField(null=True)
    sex = models.CharField(max_length=15, choices=SEXE_CHOICES, null=True)
    phone = models.CharField(max_length=35, null=True)
