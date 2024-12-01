from djongo import models

class Student(models.Model):
    usn = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    section = models.CharField(max_length=1)
    encoding = models.TextField()

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Present')

class Meta:
    db_table = 'student'

    def __str__(self):
        return f'{self.student.name} - {self.date} - {self.status}'
