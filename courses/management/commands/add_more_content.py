from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson, LearningPath, PathCourse

User = get_user_model()

class Command(BaseCommand):
    help = 'Adds more specific courses to Learning Paths'

    def handle(self, *args, **kwargs):
        instructor = User.objects.filter(role='instructor').first()
        if not instructor:
            self.stdout.write(self.style.ERROR('No instructor found. Run populate_courses first.'))
            return

        # 1. Create New Courses
        courses_data = [
            {
                'title': 'modern JavaScript Essentials',
                'desc': 'Deep dive into ES6+, Async/Await, and DOM manipulation.',
                'image': 'https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?auto=format&fit=crop&q=80',
                'price': '$49.99',
                'category': 'Development'
            },
            {
                'title': 'Advanced Django Patterns',
                'desc': 'Master CBVs, Middleware, Signals, and Deployment.',
                'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&q=80',
                'price': '$89.99',
                'category': 'Development'
            },
            {
                'title': 'Statistics for Data Science',
                'desc': 'Probability, distributions, hypothesis testing and regression analysis.',
                'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80',
                'price': '$39.99',
                'category': 'Data Science'
            },
            {
                'title': 'Deep Learning with PyTorch',
                'desc': 'Build neural networks, CNNs, and NLP models from scratch.',
                'image': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80',
                'price': '$99.99',
                'category': 'Data Science'
            }
        ]

        created_courses = {}
        for c in courses_data:
            course, created = Course.objects.get_or_create(
                title=c['title'],
                defaults={
                    'description': c['desc'],
                    'instructor': instructor,
                    'image': c['image'],
                    'price': c['price'],
                    'category': c['category']
                }
            )
            created_courses[c['title']] = course
            
            if created:
                # Add basic modules
                for i in range(1, 4):
                    mod = Module.objects.create(course=course, title=f"Module {i}: Core Concepts", order=i)
                    Lesson.objects.create(module=mod, title="Introduction", content="Welcome to this lesson.", order=1, video_url="https://www.youtube.com/embed/dQw4w9WgXcQ")
                    Lesson.objects.create(module=mod, title="Advanced Topic", content="Deep dive.", order=2, video_url="https://www.youtube.com/embed/dQw4w9WgXcQ")
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
            else:
                self.stdout.write(f'Course already exists: {course.title}')

        # 2. Update Paths
        # Retrieve existing courses (from previous populate)
        python_course = Course.objects.filter(title__icontains='Python').first()
        web_course = Course.objects.filter(title__icontains='Web').first()
        data_course = Course.objects.filter(title__icontains='Data Science Bootcamp').first()

        # Update Full-Stack Architect Path
        fs_path = LearningPath.objects.filter(title='Full-Stack Architect').first()
        if fs_path:
            # Clear existing to re-order cleanly
            PathCourse.objects.filter(path=fs_path).delete()
            
            # New Order: JS -> Python -> Django -> Web Dev
            order = 1
            if 'modern JavaScript Essentials' in created_courses:
                PathCourse.objects.create(path=fs_path, course=created_courses['modern JavaScript Essentials'], order=order)
                order += 1
            if python_course:
                PathCourse.objects.create(path=fs_path, course=python_course, order=order)
                order += 1
            if 'Advanced Django Patterns' in created_courses:
                PathCourse.objects.create(path=fs_path, course=created_courses['Advanced Django Patterns'], order=order)
                order += 1
            if web_course:
                PathCourse.objects.create(path=fs_path, course=web_course, order=order)
                
            self.stdout.write(self.style.SUCCESS('Updated Full-Stack Path with 4 courses.'))

        # Update Data Scientist Path
        ds_path = LearningPath.objects.filter(title='Data Scientist').first()
        if ds_path:
            PathCourse.objects.filter(path=ds_path).delete()
            
            # New Order: Python -> Statistics -> Data Science -> Deep Learning
            order = 1
            if python_course:
                PathCourse.objects.create(path=ds_path, course=python_course, order=order)
                order += 1
            if 'Statistics for Data Science' in created_courses:
                PathCourse.objects.create(path=ds_path, course=created_courses['Statistics for Data Science'], order=order)
                order += 1
            if data_course:
                PathCourse.objects.create(path=ds_path, course=data_course, order=order)
                order += 1
            if 'Deep Learning with PyTorch' in created_courses:
                PathCourse.objects.create(path=ds_path, course=created_courses['Deep Learning with PyTorch'], order=order)
                
            self.stdout.write(self.style.SUCCESS('Updated Data Scientist Path with 4 courses.'))
