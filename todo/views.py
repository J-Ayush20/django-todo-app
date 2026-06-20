from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm


def todo_list(request):
    """Sab todos dikhao"""
    todos = Todo.objects.all()
    completed_count = Todo.objects.filter(completed=True).count()
    pending_count = Todo.objects.filter(completed=False).count()

    context = {
        'todos': todos,
        'completed_count': completed_count,
        'pending_count': pending_count,
    }

    return render(request, 'todo_list.html', context)


def create_todo(request):
    """Naya todo banana"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()

    return render(request, 'create_todo.html', {'form': form})


def edit_todo(request, pk):
    """Todo edit karna"""
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)

    return render(request, 'edit_todo.html', {'form': form, 'todo': todo})


def toggle_todo(request, pk):
    """Todo complete/pending toggle karna"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()

    return redirect('todo_list')


def delete_todo(request, pk):
    """Todo delete karna"""
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')

    return render(request, 'confirm_delete.html', {'todo': todo})