from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment, Certificate, LearningPath, UserLearningPath
from django.db.models import Count, Q

User = get_user_model()

@login_required
def dashboard(request):
    """
    Redirects based on role, or shows Student Dashboard.
    """
    if request.user.role == 'admin' or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.role == 'instructor':
        return redirect('instructor_dashboard')
    
    # Student Dashboard Logic
    # 1. Active Enrollments (sorted by most recently accessed)
    # Optimization: Select related course and instructor to prevent N+1 queries in loop
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor').order_by('-last_accessed')
    
    # 2. Certificates
    certificates = Certificate.objects.filter(user=request.user)
    
    # 3. Suggested Courses (exclude enrolled courses)
    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    suggested_courses = Course.objects.exclude(id__in=enrolled_course_ids).order_by('-created_at')[:3]
    
    # 4. Active Paths
    active_paths = UserLearningPath.objects.filter(user=request.user).select_related('path')

    context = {
        'enrollments': enrollments,
        'enrolled_count': enrollments.filter(progress__lt=100).count(),
        'completed_count': enrollments.filter(progress=100).count(),
        'certificates': certificates,
        'cert_count': certificates.count(),
        'suggested_courses': suggested_courses,
        'active_paths': active_paths,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def admin_dashboard(request):
    """
    Full control dashboard for Admins.
    """
    if not (request.user.role == 'admin' or request.user.is_superuser):
        messages.error(request, "Access Denied: Admin Level Clearance Required.")
        return redirect('dashboard')
        
    user_stats = User.objects.aggregate(
        total=Count('id'),
        students=Count('id', filter=Q(role='student')),
        instructors=Count('id', filter=Q(role='instructor'))
    )

    context = {
        'total_users': user_stats['total'],
        'total_students': user_stats['students'],
        'total_instructors': user_stats['instructors'],
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'courses': Course.objects.all().select_related('instructor').annotate(modules_count=Count('modules')).order_by('-created_at')[:5],
        'users': User.objects.all().order_by('-date_joined')[:10],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def instructor_dashboard(request):
    """
    Course management for Instructors.
    """
    if request.user.role not in ['instructor', 'admin'] and not request.user.is_superuser:
        return redirect('dashboard')

    my_courses = Course.objects.filter(instructor=request.user).annotate(
        modules_count=Count('modules', distinct=True),
        students_count=Count('enrollments', distinct=True)
    )
    
    # Simple analytics
    total_students = Enrollment.objects.filter(course__in=my_courses).count()
    
    context = {
        'courses': my_courses,
        'total_students': total_students,
        'course_count': my_courses.count(),
    }
    return render(request, 'dashboard/instructor_dashboard.html', context)

@login_required
def manage_users(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/manage_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')
        
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
         messages.error(request, "Cannot delete Superuser.")
    else:
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
        
    return redirect('manage_users')

@login_required
def export_users_csv(request):
    if not (request.user.role == 'admin' or request.user.is_superuser):
        return redirect('dashboard')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role', 'Date Joined', 'Active'])
    
    users = User.objects.all().values_list('username', 'email', 'role', 'date_joined', 'is_active')
    for user in users:
        writer.writerow(user)
        
    return response

@login_required
def notifications(request):
    return render(request, 'dashboard/notifications.html')

@login_required
def achievements(request):
    return render(request, 'dashboard/achievements.html')

@login_required
def daily_checkin(request):
    request.user.xp += 10
    request.user.save()
    messages.success(request, f"Daily check-in complete! +10 XP. You are now Level {request.user.level}!")
    return redirect('dashboard')

@login_required
def ai_paths(request):
    paths = LearningPath.objects.all().prefetch_related('courses')
    return render(request, 'dashboard/ai_paths.html', {'paths': paths})

@login_required
def join_path(request, path_id):
    path = get_object_or_404(LearningPath, pk=path_id)
    
    # Register user on this path
    UserLearningPath.objects.get_or_create(user=request.user, path=path)

    # Find first un-enrolled course in the path
    courses = path.courses.all().order_by('pathcourse__order')
    
    target_course = None
    for course in courses:
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            target_course = course
            break
    
    # If enrolled in all, go to the first one (or last accessed logic could be better, but simple for now)
    if not target_course:
        target_course = courses.first()
        
    if target_course:
        # Auto-enroll if needed (enroll view logic duplicated here or redirect to enroll view?)
        # Let's redirect to enroll view which handles get_or_create
        return redirect('enroll', pk=target_course.pk)
    
    messages.info(request, "This path has no courses yet.")
    return redirect('ai_paths')

@login_required
def community(request):
    return render(request, 'dashboard/community.html')
