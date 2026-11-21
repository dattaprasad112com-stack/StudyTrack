
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Subject, StudyTask, StudySession, StudySchedule


# DASHBOARD
@login_required
def home(request):
    total_subjects = Subject.objects.filter(
        user=request.user
    ).count()

    pending_tasks = StudyTask.objects.filter(
        user=request.user,
        completed=False
    ).count()

    completed_tasks = StudyTask.objects.filter(
        user=request.user,
        completed=True
    ).count()

    total_hours = StudySession.objects.filter(
        user=request.user
    ).aggregate(
        total=models.Sum('hours')
    )['total'] or 0

    return render(request, 'planner/home.html', {
        'total_subjects': total_subjects,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'total_hours': total_hours,
    })


# STUDENT REGISTRATION
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'

    return render(request, 'planner/register.html', {'form': form})


# STUDENT LOGIN
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'

        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'

    return render(request, 'planner/login.html', {'form': form})


# STUDENT LOGOUT
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('home')


# VIEW SUBJECTS
@login_required
def subjects(request):
    all_subjects = Subject.objects.filter(user=request.user)

    return render(request, 'planner/subjects.html', {
        'subjects': all_subjects
    })


# ADD SUBJECT
@login_required
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name and name.strip():
            Subject.objects.create(
                user=request.user,
                name=name.strip(),
                description=description
            )

        return redirect('subjects')

    return render(request, 'planner/add_subject.html')


# EDIT SUBJECT
@login_required
def edit_subject(request, id):
    subject = Subject.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.description = request.POST.get('description')
        subject.save()
        return redirect('subjects')

    return render(request, 'planner/edit_subject.html', {
        'subject': subject
    })


# DELETE SUBJECT
@login_required
def delete_subject(request, id):
    subject = Subject.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        subject.delete()

    return redirect('subjects')


# VIEW STUDY SCHEDULE
@login_required
def schedule_list(request):
    schedules = StudySchedule.objects.filter(
        user=request.user
    ).order_by('date', 'start_time')

    return render(request, 'planner/schedule.html', {
        'schedules': schedules
    })


# ADD STUDY SCHEDULE
@login_required
def add_schedule(request):
    subjects = Subject.objects.filter(user=request.user)

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        title = request.POST.get('title')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if subject_id and title and date and start_time and end_time:
            subject = subjects.filter(id=subject_id).first()

            if subject and end_time > start_time:
                StudySchedule.objects.create(
                    user=request.user,
                    subject=subject,
                    title=title,
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
                return redirect('schedule')

    return render(request, 'planner/add_schedule.html', {
        'subjects': subjects
    })


# VIEW STUDY TASKS
@login_required
def task_list(request):
    tasks = StudyTask.objects.filter(
        user=request.user
    ).order_by('date')

    return render(request, 'planner/tasks.html', {
        'tasks': tasks
    })


# ADD STUDY TASK
@login_required
def add_task(request):
    subjects = Subject.objects.filter(user=request.user)

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        title = request.POST.get('title')
        date = request.POST.get('date')

        subject = subjects.filter(id=subject_id).first()

        if subject and title and date:
            StudyTask.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                date=date
            )
            return redirect('tasks')

    return render(request, 'planner/add_task.html', {
        'subjects': subjects
    })


# COMPLETE OR UNDO TASK
@login_required
def complete_task(request, id):
    task = StudyTask.objects.filter(
        id=id,
        user=request.user
    ).first()

    if task and request.method == 'POST':
        task.completed = not task.completed
        task.save()

    return redirect('tasks')


# DELETE STUDY TASK
@login_required
def delete_task(request, id):
    task = StudyTask.objects.filter(
        id=id,
        user=request.user
    ).first()

    if task and request.method == 'POST':
        task.delete()

    return redirect('tasks')


@login_required
def progress_report(request):
    total_tasks = StudyTask.objects.filter(
        user=request.user
    ).count()

    completed_tasks = StudyTask.objects.filter(
        user=request.user,
        completed=True
    ).count()

    pending_tasks = StudyTask.objects.filter(
        user=request.user,
        completed=False
    ).count()

    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_percentage = 0

    subjects = Subject.objects.filter(user=request.user)

    subject_data = []

    for subject in subjects:
        total = StudyTask.objects.filter(
            user=request.user,
            subject=subject
        ).count()

        completed = StudyTask.objects.filter(
            user=request.user,
            subject=subject,
            completed=True
        ).count()

        subject_data.append({
            'name': subject.name,
            'total': total,
            'completed': completed,
        })

    return render(request, 'planner/progress.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage,
        'subject_data': subject_data,
    })


@login_required
def study_hours(request):
    sessions = StudySession.objects.filter(
        user=request.user
    ).order_by('-date')

    total_hours = sessions.aggregate(
        total=models.Sum('hours')
    )['total'] or 0

    return render(request, 'planner/study_hours.html', {
        'sessions': sessions,
        'total_hours': total_hours,
    })


@login_required
def add_study_session(request):
    subjects = Subject.objects.filter(user=request.user)

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        hours = request.POST.get('hours')

        subject = subjects.filter(id=subject_id).first()

        try:
            hours = float(hours)
        except (TypeError, ValueError):
            hours = 0

        if subject and date and hours > 0:
            StudySession.objects.create(
                user=request.user,
                subject=subject,
                date=date,
                hours=hours
            )
            return redirect('study_hours')

        messages.error(request, 'Please enter valid study details.')

    return render(request, 'planner/add_study_session.html', {
        'subjects': subjects,
    })



@login_required
def account_settings(request):

    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':

        action = request.POST.get('action')

        # Update email
        if action == 'update_email':
            email = request.POST.get('email', '').strip()

            if email:
                request.user.email = email
                request.user.save()
                messages.success(request, 'Email updated successfully!')
            else:
                messages.error(request, 'Please enter a valid email.')

        # Change password
        elif action == 'change_password':
            password_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                return redirect('settings')

        return redirect('settings')

    return render(request, 'planner/settings.html', {
        'password_form': password_form,
    })
