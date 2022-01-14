from django.db import models

class Department(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_head = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dept_id} {self.dept_name} {self.dept_head}"

class Student(models.Model):
    std_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    departments = models.ManyToManyField(Department, related_name="dept")

    def __str__(self):
        return f"{self.std_id} {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"