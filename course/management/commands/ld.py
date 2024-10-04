from django.core.management.base import BaseCommand
from course.models import Course, Review, Discussion, Subject
from django.contrib.auth.models import User
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Load dummy data into the database'

    def handle(self, *args, **kwargs):
        # Create a user for the reviews and discussions
        user, created = User.objects.get_or_create(username='johndoe', password='password123')

        # Example of creating a course
        course = Course.objects.create(
            course_name='Intro',
            course_length=30,  # Duration in days
            course_price=299.99,
            start_date=date.today(),
            subject = Subject.objects.get_or_create(name='CS'),
            end_date=date.today() + timedelta(days=30),
            exam_date=date.today() + timedelta(days=35),
            enrollment_end_date=date.today() + timedelta(days=5),
            exam_registration_end_date=date.today() + timedelta(days=10),
            ug_pg='UG',
            core_elective='Core',
            course_type='FDP',
            domain='Computer Science',
            join_link='http://example.com/join',
            old_course_url='http://example.com/old-course',
            nptel_url='http://nptel.ac.in/courses/xyz'
        )

        # Create a review for the course
        Review.objects.create(
            course=course,
            user=user,
            rating=5,
            comment='Great course for beginners!'
        )

        # Create a discussion for the course
        Discussion.objects.create(
            course=course,
            user=user.username,  # Using the username directly here
            content='What are the prerequisites for this course?'
        )

        self.stdout.write(self.style.SUCCESS('Dummy data loaded successfully!'))
