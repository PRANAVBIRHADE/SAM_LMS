from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson, Enrollment
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Enrollment.objects.all().delete()
        Lesson.objects.all().delete()
        Module.objects.all().delete()
        Course.objects.all().delete()
        User.objects.filter(role__in=['student', 'instructor']).delete()

        self.stdout.write('Creating users...')
        instructor = User.objects.create_user(username='instructor', email='instructor@tpoint.tech', password='password123', role='instructor')
        student = User.objects.create_user(username='student', email='student@tpoint.tech', password='password123', role='student')
        
        # Course 1: Python
        self.stdout.write('Creating Python Course...')
        c1 = Course.objects.create(
            title='Complete Python Mastery',
            description='Master Python 3 from scratch to advanced concepts. Learn Data Science, Django, and more.',
            instructor=instructor,
            price=49.99,
            # No thumbnail for now, relying on placeholder in template
        )
        m1 = Module.objects.create(course=c1, title='Introduction to Python', order=1)
        Lesson.objects.create(module=m1, title='Installing Python', order=1)
        Lesson.objects.create(module=m1, title='Variables and Data Types', order=2)
        
        m2 = Module.objects.create(course=c1, title='Data Structures', order=2)
        Lesson.objects.create(module=m2, title='Lists and Tuples', order=1)
        
        # Course 2: React
        self.stdout.write('Creating React Course...')
        c2 = Course.objects.create(
            title='React JS: The Complete Guide',
            description='Dive in and learn React.js from scratch! Learn Reactjs, Hooks, Redux, React Routing, Animations, Next.js and way more!',
            instructor=instructor,
            price=89.99,
        )
        m3 = Module.objects.create(course=c2, title='React Basics', order=1)
        Lesson.objects.create(module=m3, title='What is React?', order=1)
        Lesson.objects.create(module=m3, title='JSX Explained', order=2)

        # Course 3: SQL
        self.stdout.write('Creating SQL Course...')
        c3 = Course.objects.create(
            title='SQL & Database Management',
            description='Learn SQL from scratch. Master database design, complex queries, and postgreSQL.',
            instructor=instructor,
            price=39.99,
        )
        
        # Enroll Student
        self.stdout.write('Enrolling student...')
        Enrollment.objects.create(student=student, course=c1, progress=15.0)

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))
