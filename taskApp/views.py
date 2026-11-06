from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

# 1. User Registration View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 2. Read (শুধু লগইন করা ইউজারের টাস্ক দেখাবে)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'task_list.html', {'tasks': tasks})

# 3. Create (টাস্কের সাথে ইউজার, প্রায়োরিটি, ক্যাটাগরি ও ডেডলাইন যুক্ত করা)
@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category', 'General')
        priority = request.POST.get('priority', 'Medium')
        due_date = request.POST.get('due_date') or None
        
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                category=category,
                priority=priority,
                due_date=due_date
            )
        return redirect('task_list')
    return render(request, 'task_form.html')

# 4. Update
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.category = request.POST.get('category', 'General')
        task.priority = request.POST.get('priority', 'Medium')
        task.due_date = request.POST.get('due_date') or None
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    return render(request, 'task_form.html', {'task': task})

# 5. Delete
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})