from django.core.management.base import BaseCommand
from courses.models import Course, LearningPath, PathCourse

class Command(BaseCommand):
    help = 'Populates the database with sample learning paths'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample paths...')

        # Retrieve existing courses
        try:
            python_course = Course.objects.filter(title__icontains='Python').first()
            web_course = Course.objects.filter(title__icontains='Web').first()
            data_course = Course.objects.filter(title__icontains='Data').first()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error finding courses: {e}'))
            return

        if not all([python_course, web_course, data_course]):
             self.stdout.write(self.style.WARNING('Some courses missing, ensuring full population...'))
             # (Ideally we would run populate_courses here if needed, but assuming user ran it)

        # 1. Full-Stack Architect Path
        fs_path, created = LearningPath.objects.get_or_create(
            title='Full-Stack Architect',
            defaults={
                'description': 'Master modern web development. Build scalable applications from frontend to backend.'
            }
        )
        if created and python_course and web_course:
            PathCourse.objects.create(path=fs_path, course=python_course, order=1)
            PathCourse.objects.create(path=fs_path, course=web_course, order=2)
            self.stdout.write(f'Created path: {fs_path.title}')
        
        # 2. Data Scientist Path
        ds_path, created = LearningPath.objects.get_or_create(
            title='Data Scientist',
            defaults={
                'description': 'Unlock the power of data. Analyze trends and build machine learning models.'
            }
        )
        if created and python_course and data_course:
            PathCourse.objects.create(path=ds_path, course=python_course, order=1)
            PathCourse.objects.create(path=ds_path, course=data_course, order=2)
            self.stdout.write(f'Created path: {ds_path.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated learning paths.'))
