from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    xp = models.PositiveIntegerField(default=0)

    @property
    def level(self):
        # simple level formula: 100 XP per level. Level 1 starts at 0 XP.
        return (self.xp // 100) + 1

    def __str__(self):
        return f"{self.username} ({self.role})"
