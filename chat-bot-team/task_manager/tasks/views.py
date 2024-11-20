from django.shortcuts import render, redirect
from .models import Task

def home(request):
    if request.method == "POST":
        colleague_name = request.POST.get('colleague_name')
        task_desc = request.POST.get('task_desc')
        # Добавление новой задачи
        if colleague_name and task_desc:
            Task.objects.create(colleague_name=colleague_name, task_desc=task_desc)
            return redirect('home')

    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def colleague_tasks(request, colleague_name):
    tasks = Task.objects.filter(colleague_name=colleague_name)
    return render(request, 'tasks/colleague_tasks.html', {'tasks': tasks, 'colleague_name': colleague_name})
