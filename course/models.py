from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institute(models.Model):
    name = models.CharField(max_length=200)
    coordinator = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    cid = models.CharField(max_length=50, null=True)
    course_name = models.CharField(max_length=200)
    course_length = models.CharField(max_length=100, null=True)  # Length in weeks
    course_price = models.DecimalField(max_digits=10, decimal_places=2)  # Example: 299.99
    subjects = models.ManyToManyField(Subject, related_name='courses')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='courses',null=True)  # Link to institution
    teacher_name = models.CharField(max_length=200,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_date = models.DateField()
    nptel_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.course_name



class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    user = models.CharField(max_length=100)  # or use a ForeignKey to a User model for user accounts
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion on {self.course.course_name} by {self.user}"
    
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating from 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.course.course_name} by {self.user.username}"