from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название проекта'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание проекта'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name='projects',
        verbose_name='Участники проекта'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_REVIEW = 'review'
    STATUS_DONE = 'done'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_REVIEW, 'На проверке'),
        (STATUS_DONE, 'Завершена'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название задачи'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание задачи'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Исполнитель'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name='Статус'
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name='Срок выполнения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title