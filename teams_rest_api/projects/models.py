from django.db import models


class Project(models.Model):
    name = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        null=True,
    )
    project_members = models.ManyToManyField(
        'users.User',
        related_name='contributing_projects',
        blank=True,
    )

    def __str__(self):
        return self.name


class Invitation(models.Model):
    sender = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='sent_by',
    )
    invitee = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='invitee',
    )
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='invitations',
    )


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
    due_date = models.DateField()
    assignee = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True,
    )
    creator = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
    )

    def __str__(self):
        return self.name
