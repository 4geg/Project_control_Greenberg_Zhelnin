from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, Task
from .forms import ProjectForm, TaskForm


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    status_filter = request.GET.get('status')

    tasks = project.tasks.all()

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(
        request,
        'core/project_detail.html',
        {
            'project': project,
            'tasks': tasks,
            'status_filter': status_filter,
            'status_choices': Task.STATUS_CHOICES,
        }
    )


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()
            project.members.add(request.user)
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(
        request,
        'core/project_form.html',
        {
            'form': form,
            'title': 'Создание проекта',
        }
    )


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'core/project_form.html',
        {
            'form': form,
            'title': 'Редактирование проекта',
        }
    )


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(
        request,
        'core/project_confirm_delete.html',
        {
            'project': project,
        }
    )


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(
        request,
        'core/task_form.html',
        {
            'form': form,
            'project': project,
            'title': 'Создание задачи',
        }
    )


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        'core/task_form.html',
        {
            'form': form,
            'project': task.project,
            'title': 'Редактирование задачи',
        }
    )


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id

    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=project_id)

    return render(
        request,
        'core/task_confirm_delete.html',
        {
            'task': task,
        }
    )