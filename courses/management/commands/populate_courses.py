from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Ensure an instructor exists
        instructor, created = User.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@example.com',
                'role': 'instructor',
                'is_staff': True
            }
        )
        if created:
            instructor.set_password('password123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS('Created instructor user.'))
        else:
            self.stdout.write('Using existing instructor user.')

        # Sample Courses Data
        courses_data = [
            {
                'title': 'Python Mastery: From Zero to Hero',
                'description': 'Master Python programming with this comprehensive course. Learn data structures, algorithms, and build real-world applications.',
                'price': 49.99,
                'modules': [
                    {'title': 'Introduction to Python', 'lessons': ['Setting up Environment', 'Variables and Data Types', 'Control Flow']},
                    {'title': 'Data Structures', 'lessons': ['Lists and Tuples', 'Dictionaries and Sets', 'List Comprehensions']},
                    {'title': 'Object Oriented Programming', 'lessons': ['Classes and Objects', 'Inheritance', 'Polymorphism']}
                ]
            },
            {
                'title': 'Full-Stack Web Development',
                'description': 'Become a full-stack developer. Covers HTML, CSS, JavaScript, React, and Django.',
                'price': 89.99,
                'modules': [
                    {'title': 'Frontend Fundamentals', 'lessons': ['HTML5 Semantic Structure', 'CSS3 Styling', 'JavaScript Basics']},
                    {'title': 'React.js', 'lessons': ['Components and Props', 'State Management', 'Hooks']},
                    {'title': 'Backend with Django', 'lessons': ['Django Views and URLs', 'Models and ORM', 'Authentication']}
                ]
            },
            {
                'title': 'Data Science Bootcamp',
                'description': 'Learn how to analyze data, create visualizations, and build machine learning models.',
                'price': 69.99,
                'modules': [
                    {'title': 'NumPy and Pandas', 'lessons': ['NumPy Arrays', 'Pandas DataFrames', 'Data Cleaning']},
                    {'title': 'Data Visualization', 'lessons': ['Matplotlib', 'Seaborn', 'Interactive Plots']},
                    {'title': 'Machine Learning', 'lessons': ['Linear Regression', 'Classification', 'Clustering']}
                ]
            }
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                instructor=instructor,
                defaults={
                    'description': course_data['description'],
                    'price': course_data['price']
                }
            )
            
            if created:
                self.stdout.write(f"Created course: {course.title}")
                for i, module_data in enumerate(course_data['modules'], 1):
                    module = Module.objects.create(
                        course=course,
                        title=module_data['title'],
                        order=i
                    )
                    for j, lesson_title in enumerate(module_data['lessons'], 1):
                        Lesson.objects.create(
                            module=module,
                            title=lesson_title,
                            content=f"Content for {lesson_title}. This is a sample lesson.",
                            order=j
                        )
            else:
                self.stdout.write(f"Course already exists: {course.title}")

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample courses.'))
