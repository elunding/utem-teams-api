from django.db import models


class Project(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):

    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    class Status(models.TextChoices):
        TODO = 'TD',
        IN_PROGRESS = 'IP',
        DONE = 'DN',

    name = models.TextField()
    description = models.TextField()
    priority = models.IntegerField(choices=Priority.choices)
    status = models.CharField(
        choices=Status.choices,
        max_length=2,
        default='TD',
    )
    project = models.ForeignKey(
        Project,
        related_name='tasks',
        on_delete=models.CASCADE,
    )
