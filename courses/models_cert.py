from django.db import models
from django.conf import settings
import uuid

# ... (Existing imports: Course, Module, Lesson, Enrollment, Quiz, Question, UserQuizAttempt)

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"
