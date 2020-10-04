from django.db import models


class Project(models.Model):
    name = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = (
        (1, 'LOW'),
        (2, 'MEDIUM'),
        (3, 'HIGH'),
    )

    STATUS_CHOICES = (
        ('TD', 'TODO'),
        ('IP', 'IN_PROGRESS'),
        ('DN', 'DONE'),
    )

    name = models.TextField()
    description = models.TextField()
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=1,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=2,
        default='TD',
    )
    project = models.ForeignKey(
        Project,
        related_name='tasks',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
