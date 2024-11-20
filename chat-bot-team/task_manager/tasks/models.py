from django.db import models

class Task(models.Model):
    colleague_name = models.CharField(max_length=100)
    task_desc = models.TextField()

    def __str__(self):
        return f"{self.colleague_name}: {self.task_desc}"

