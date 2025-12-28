from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment, Quiz, Question, UserQuizAttempt
from .models import Course, Module, Lesson, Enrollment, Quiz, Question, UserQuizAttempt, Certificate
from .forms import CourseForm, ModuleForm, LessonForm, QuizForm, QuestionForm
from django.db.models import Count

# ... (Existing views)

@login_required
def generate_certificate(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    if enrollment.progress < 100:
        messages.error(request, "You must complete 100% of the course to get certified.")
        return redirect('dashboard')
        
    certificate, created = Certificate.objects.get_or_create(
        user=request.user, 
        course=course
    )
    
    return render(request, 'courses/certificate.html', {'certificate': certificate})


# ... (Existing views)

@login_required
def add_quiz(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user != course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, f"Quiz '{quiz.title}' created! Add questions.")
            return redirect('add_question', quiz_pk=quiz.pk)
    else:
        form = QuizForm()
        
    return render(request, 'courses/simple_form.html', {'form': form, 'title': f'Create Quiz for {course.title}'})

@login_required
def add_question(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.user != quiz.course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question added!")
            return redirect('add_question', quiz_pk=quiz.pk)
    else:
        form = QuestionForm()
        
    return render(request, 'courses/add_question.html', {'form': form, 'quiz': quiz, 'questions': questions})


# ... (Existing views)

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # Ensure user is enrolled
    # (Simplified: assumes public for now or relies on dashboard link visibility)
    
    if request.method == 'POST':
        score = 0
        total = quiz.questions.count()
        
        for question in quiz.questions.all():
            selected = request.POST.get(f'question_{question.id}')
            if selected == question.correct_option:
                score += 1
                
        percentage = int((score / total) * 100) if total > 0 else 0
        passed = percentage >= quiz.pass_score
        
        UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=percentage,
            passed=passed
        )
        
        context = {
            'quiz': quiz,
            'percentage': percentage,
            'passed': passed,
            'score': score,
            'total': total
        }
        return render(request, 'courses/quiz_result.html', context)
        
    return render(request, 'courses/quiz_take.html', {'quiz': quiz})


# ... (Existing views: course_list, course_detail, lesson_detail)

@login_required
def create_course(request):
    if request.user.role not in ['instructor', 'admin'] and not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f"Course '{course.title}' created! Add modules now.")
            return redirect('manage_course_content', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create New Course'})

@login_required
def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Allow Instructor (owner), Admin, or Superuser
    if request.user != course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
        
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

@login_required
def manage_course_content(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
    
    return render(request, 'courses/manage_content.html', {'course': course})

@login_required
def add_module(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user != course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, "Module added!")
            return redirect('manage_course_content', pk=course.pk)
    else:
        form = ModuleForm()
        
    return render(request, 'courses/simple_form.html', {'form': form, 'title': f'Add Module to {course.title}'})

@login_required
def add_lesson(request, module_pk):
    module = get_object_or_404(Module, pk=module_pk)
    if request.user != module.course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, "Lesson added!")
            return redirect('manage_course_content', pk=module.course.pk)
    else:
        form = LessonForm()
        
    return render(request, 'courses/simple_form.html', {'form': form, 'title': f'Add Lesson to {module.title}'})

@login_required
def edit_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.user != module.course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, "Module updated!")
            return redirect('manage_course_content', pk=module.course.pk)
    else:
        form = ModuleForm(instance=module)
        
    return render(request, 'courses/simple_form.html', {'form': form, 'title': f'Edit Module: {module.title}'})

@login_required
def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.user != lesson.module.course.instructor and request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated!")
            return redirect('manage_course_content', pk=lesson.module.course.pk)
    else:
        form = LessonForm(instance=lesson)
        
    return render(request, 'courses/simple_form.html', {'form': form, 'title': f'Edit Lesson: {lesson.title}'})


def course_list(request):
    courses = Course.objects.all().select_related('instructor').annotate(modules_count=Count('modules'))
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

def lesson_detail(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    # Ensure lesson belongs to course
    # (Simplified for now, in production check relation)
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course, 
        'lesson': lesson
    })

@login_required
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"Welcome to the {course.title} program.")
    return redirect('dashboard')
