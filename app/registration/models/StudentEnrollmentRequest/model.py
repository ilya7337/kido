from django.db import models
from registration.models.User.model import User

class StudentEnrollmentRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    trainer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='trainer_requests',
        limit_choices_to={'role': 'trainer'}
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = StudentEnrollmentRequest.objects.get(pk=self.pk).status
        else:
            old_status = None

        super().save(*args, **kwargs)

        if old_status != self.status and self.status == self.REJECTED:
            # Удаляем пользователя и заявку, если заявка отклонена
            self.student.delete()
            self.delete()
        elif old_status != self.status and self.status == self.APPROVED:
            # Удаляем заявку, если заявка принята
            self.delete()
        

    def __str__(self):
        return f"{self.trainer} -> {self.student} ({self.status})"
    

    