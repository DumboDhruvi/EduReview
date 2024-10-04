from django.core.management.base import BaseCommand
from course.models import Subject

class Command(BaseCommand):
    help = 'Create some sample subjects'

    def handle(self, *args, **kwargs):
        subjects = ['Mathematics', 'Physics', 'Chemistry', 'dick']
        
        for subject_name in subjects:
            subject, created = Subject.objects.get_or_create(name=subject_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created subject: {subject_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Subject already exists: {subject_name}'))
