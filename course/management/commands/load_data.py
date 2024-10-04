import pandas as pd
from django.core.management.base import BaseCommand
from course.models import Course, Subject, Institute

class Command(BaseCommand):
    help = 'Load courses from an Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel file, skipping the first 10 rows
        df = pd.read_excel(r'C:\Users\dhruv\OneDrive\Desktop\review website\eduReview\course\management\commands\database.xlsx', skiprows=10)

        # Loop through each row and load data into the model
        for index, row in df.iterrows():
            # Get or create the subject
            subject_name = row['subjects'].strip()
            subject, created = Subject.objects.get_or_create(name=subject_name)

            # Get or create the institute
            institute_name = row['institute'].strip()
            institute, created = Institute.objects.get_or_create(name=institute_name)

            # Create the Course object
            course = Course.objects.create(
                cid=row.get('cid', None),  # Handle optional 'cid'
                course_name=row['course_name'],
                course_length= row['course_length'],
                course_price = 1000,
                teacher_name=row.get('teacher_name', None),  # Handle optional field
                start_date=row['start_date'],
                end_date=row['end_date'],
                exam_date=row['exam_date'],
                nptel_url=row.get('nptel_url', '')  # Handle optional field
            )

            # Add the subject and institute to the course
            course.subjects.add(subject)
            course.institute = institute
            course.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully added course: {course.course_name}'))

