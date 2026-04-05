from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from todos.forms import PersonForm, TodoForm
from todos.models import Person, Todo


# Create your views here.
def hello_world_view(request):
    return HttpResponse("Hello, World!".encode())


def hello_html_view(request):
    return render(request, "todos/hello.html")


def hello_path(request, name):
    return HttpResponse(f"Hello, {name}!".encode())


def hello_query(request):
    return HttpResponse(f"Hello, {request.GET.get('name')}!".encode())


def redirect_view(request):
    return redirect("hello_html")


def post_example(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            age = form.cleaned_data.get("age")
            job = form.cleaned_data.get("job")

            return HttpResponse(
                f"Hello, {name}! You are {age} years old. You work as a {job}.".encode()
            )

    return HttpResponseNotAllowed(["POST"])


def submit_example(request):
    return render(request, "todos/submit.html")


def submit_django_form(request):
    form = PersonForm()
    return render(request, "todos/submit_django_form.html", {"form": form})


def template_view(request):
    context = {
        "name": "Zen",
        "age": 333,
        "skills": [
            "Software Engineer",
            "Python Developer",
            # "Java",
            "Rust",
        ],
    }
    return render(request, "todos/template_demo.html", context)


def todos(request):
    if request.method == "POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save()
            return HttpResponse("Todo created successfully!".encode())
    else:
        form = TodoForm()
        todos = Todo.objects.all()
        return render(request, "todos/todos.html", {"form": form, "todos": todos})


def person_details(request, person_id):
    person = Person.objects.filter(id=person_id).first()

    return render(request, "todos/person_details.html", {"person": person})


def delete_todo(request, todo_id):
    Todo.objects.filter(id=todo_id).delete()

    return HttpResponse("Todo deleted successfully!".encode())


def toggle_todo_done(request, todo_id):
    todo = Todo.objects.filter(id=todo_id).first()

    if todo:
        todo.done = not todo.done
        todo.save()

    return HttpResponse("Todo done status updated successfully!".encode())