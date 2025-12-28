from django import forms
from .models import Course, Module, Lesson, Quiz, Question

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 4, 'placeholder': 'Course details...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'order': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'content': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 6}),
            'video_url': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'https://youtube.com/...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'pass_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'pass_score': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'Question text...'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Option A'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Option B'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Option C'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Option D'}),
            'correct_option': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
        }
