
from django.db import models

from apps.moderation.models import Employee


class Lecture(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return (f"Lecture("
                f"id: {self.id}, "
                f"employee: {self.employee.get_name()}, "
                f"subject: {self.subject.name}, "
                f"auditorium: {self.auditorium.number}, "
                f"date: {self.date}, "
                f"start: {self.start}, "
                f"end: {self.end}"
                f")")
