from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=70)
    class Sex(models.IntegerChoices):
        MALE = 1, ('MALE')
        FEMALE = 2, ('FEMALE')
        OTHER = 3, ('OTHER')
    sex = models.IntegerField(choices=Sex.choices)
    def __str__(self):

        return self.full_name

class Homework(models.Model):
    commit_date = models.DateField(auto_now=True)
    headline = models.CharField(max_length=200)
    attach = models.FileField()
    remark = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


    def __str__(self):
        return self.headline
